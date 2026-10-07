import http.server
import socketserver
import json
import urllib.parse
import sys
import os
import traceback
from pathlib import Path

# Redirect stdout/stderr safely to a log file to avoid WinError 6 on background processes
LOG_FILE = Path(__file__).resolve().parent.parent / "web_server.log"
try:
    log_fp = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
    sys.stdout = log_fp
    sys.stderr = log_fp
except Exception:
    pass

from pcda.agent import ProofCarryingDataAnalyst
from pcda.verifier import CodeVerifier
from pcda.data_profiler import DataProfiler
from pcda.chatbot import PCDAChatbot
from pcda.config import DATA_DIR, ROOT_DIR

PORT = 8080
STATIC_DIR = Path(__file__).resolve().parent / "static"

agent = ProofCarryingDataAnalyst(DATA_DIR)
verifier = CodeVerifier()
profiler = DataProfiler(DATA_DIR)
chatbot = PCDAChatbot(DATA_DIR)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class PCDAHttpHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        try:
            sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")
        except Exception:
            pass

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            
            if parsed.path == "/" or parsed.path == "/index.html":
                return self.serve_static(STATIC_DIR / "index.html", "text/html")
            elif parsed.path == "/api/profile":
                self.send_json_response(profiler.profile_all())
                return
            elif parsed.path == "/api/benchmark":
                from tests.test_benchmark import run_all_benchmarks
                results = run_all_benchmarks()
                self.send_json_response(results)
                return
            
            # Static files
            requested_file = STATIC_DIR / parsed.path.lstrip("/")
            if requested_file.exists() and requested_file.is_file():
                mime_type = "text/plain"
                if requested_file.suffix == ".html":
                    mime_type = "text/html"
                elif requested_file.suffix == ".js":
                    mime_type = "application/javascript"
                elif requested_file.suffix == ".css":
                    mime_type = "text/css"
                return self.serve_static(requested_file, mime_type)

            self.send_error_response("Not Found", 404)
        except Exception as e:
            self.send_error_response(str(e), 500)

    def do_POST(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_error_response("Invalid JSON payload", 400)
                return

            if parsed.path == "/api/ask":
                query = data.get("query", "").strip()
                if not query:
                    self.send_error_response("Query cannot be empty", 400)
                    return
                result = agent.answer_query(query)
                self.send_json_response(result)

            elif parsed.path == "/api/verify":
                code = data.get("code", "")
                expected = data.get("expected", None)
                if expected is not None:
                    try:
                        expected = float(expected)
                    except ValueError:
                        expected = None

                if expected is not None:
                    matched, res = verifier.verify_claim(expected, code, cwd=str(ROOT_DIR))
                    self.send_json_response({
                        "success": res.success,
                        "matched": matched,
                        "verified_value": res.verified_value,
                        "execution_time_ms": res.execution_time_ms,
                        "stdout": res.stdout,
                        "stderr": res.stderr,
                        "error_message": res.error_message
                    })
                else:
                    res = verifier.execute_code(code, cwd=str(ROOT_DIR))
                    self.send_json_response({
                        "success": res.success,
                        "verified_value": res.verified_value,
                        "execution_time_ms": res.execution_time_ms,
                        "stdout": res.stdout,
                        "stderr": res.stderr,
                        "error_message": res.error_message
                    })

            elif parsed.path == "/api/chat":
                message = data.get("message", "").strip()
                history = data.get("history", [])
                if not message:
                    self.send_error_response("Message cannot be empty", 400)
                    return
                chat_res = chatbot.process_message(message, history=history)
                self.send_json_response(chat_res)

            elif parsed.path == "/api/upload":
                filename = data.get("filename", "").strip()
                content = data.get("content", "")
                if not filename or not content:
                    self.send_error_response("filename and content required", 400)
                    return
                
                safe_name = os.path.basename(filename)
                target_path = DATA_DIR / safe_name
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(content)

                profiler._load_datasets()
                agent.reload_datasets()
                chatbot.agent.reload_datasets()

                prof = profiler.profile_all()
                table_info = prof["tables"].get(safe_name, {})
                self.send_json_response({
                    "success": True,
                    "filename": safe_name,
                    "columns": table_info.get("columns", []),
                    "row_count": table_info.get("row_count", 0),
                    "profile": prof
                })
            else:
                self.send_error_response("Not Found", 404)
        except Exception as e:
            self.send_error_response(str(e), 500)

    def serve_static(self, filepath: Path, content_type: str):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error_response(str(e), 500)

    def send_json_response(self, data: dict, status: int = 200):
        try:
            def clean_nans(obj):
                if isinstance(obj, float):
                    if obj != obj or obj == float('inf') or obj == float('-inf'):
                        return None
                elif isinstance(obj, dict):
                    return {k: clean_nans(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [clean_nans(v) for v in obj]
                return obj

            sanitized_data = clean_nans(data)
            body = json.dumps(sanitized_data, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception:
            pass

    def send_error_response(self, message: str, status: int = 400):
        self.send_json_response({"error": message, "status": "ERROR"}, status=status)

def run_server(host: str = "0.0.0.0", port: int = PORT):
    server = ThreadedHTTPServer((host, port), PCDAHttpHandler)
    print(f"Proof-Carrying Data Analyst Web Server active on http://localhost:{port} (host={host})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    run_server()
