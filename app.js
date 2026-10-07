// Single-Page Window Controller for Proof-Carrying Data Analyst

document.addEventListener("DOMContentLoaded", () => {
  loadActiveDatasets();
});

// -------------------------------------------------------------
// DATASET UPLOAD HANDLER
// -------------------------------------------------------------
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (e) => {
    const content = e.target.result;
    appendAssistantBubble(`Uploading and profiling dataset <strong>${file.name}</strong>...`);

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: file.name, content: content })
      });
      const data = await res.json();

      if (data.success) {
        loadActiveDatasets();
        appendAssistantBubble(`
          🎉 <strong>Dataset Ingested Successfully!</strong><br>
          • <strong>File:</strong> <code>${data.filename}</code> (${data.row_count} rows)<br>
          • <strong>Columns:</strong> <code>${data.columns.join(", ")}</code><br><br>
          You can now ask questions about this dataset (e.g. <em>"What is the average ${data.columns[1] || 'value'}?"</em> or <em>"Total sum of ${data.columns[0] || 'records'}"</em>).
        `);
      } else {
        appendAssistantBubble(`<span style="color:var(--danger);">Upload failed: ${data.error || "Unknown error"}</span>`);
      }
    } catch (err) {
      appendAssistantBubble(`<span style="color:var(--danger);">Upload error: ${err.message}</span>`);
    }
  };
  reader.readAsText(file);
}

// -------------------------------------------------------------
// LOAD ACTIVE DATASETS
// -------------------------------------------------------------
async function loadActiveDatasets() {
  const container = document.getElementById("activeTablesList");
  try {
    const res = await fetch("/api/profile");
    const data = await res.json();

    let html = "";
    for (const [name, info] of Object.entries(data.tables)) {
      html += `
        <div class="table-chip">
          <span>📄 ${name}</span>
          <span style="color:var(--primary); font-size:0.7rem;">${info.row_count} rows</span>
        </div>
      `;
    }
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<span style="color:var(--danger); font-size:0.75rem;">Error loading tables</span>`;
  }
}

// -------------------------------------------------------------
// QUERY & CHAT WORKSPACE
// -------------------------------------------------------------
function quickQuery(txt) {
  document.getElementById("userQueryInput").value = txt;
  sendQuery();
}

async function sendQuery() {
  const input = document.getElementById("userQueryInput");
  const query = input.value.trim();
  if (!query) return;

  const stream = document.getElementById("chatStream");

  // User Bubble
  const userDiv = document.createElement("div");
  userDiv.className = "bubble user";
  userDiv.innerText = query;
  stream.appendChild(userDiv);
  input.value = "";

  // Loading Bubble
  const loadId = "load_" + Date.now();
  const loadDiv = document.createElement("div");
  loadDiv.id = loadId;
  loadDiv.className = "bubble assistant";
  loadDiv.innerHTML = `<span style="color:var(--primary);">PCDA is analyzing data, synthesizing code & running sandbox verification...</span>`;
  stream.appendChild(loadDiv);
  stream.scrollTop = stream.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: query })
    });
    const data = await res.json();

    const loader = document.getElementById(loadId);
    if (loader) loader.remove();

    renderAssistantResponse(data);
  } catch (err) {
    const loader = document.getElementById(loadId);
    if (loader) {
      loader.innerHTML = `<span style="color:var(--danger);">Error: ${err.message}</span>`;
    }
  }
}

function appendAssistantBubble(htmlContent) {
  const stream = document.getElementById("chatStream");
  const div = document.createElement("div");
  div.className = "bubble assistant";
  div.innerHTML = htmlContent;
  stream.appendChild(div);
  stream.scrollTop = stream.scrollHeight;
}

function renderAssistantResponse(data) {
  const stream = document.getElementById("chatStream");
  const div = document.createElement("div");
  div.className = "bubble assistant";

  let statusTag = "";
  if (data.status === "VERIFIED") {
    statusTag = `<span class="status-tag tag-verified">✓ VERIFIED WITH EXECUTABLE PROOF</span>`;
  } else if (data.status === "REFUSED") {
    statusTag = `<span class="status-tag tag-refused">🛡️ REFUSED (GUARDRAIL ACTIVE)</span>`;
  } else {
    statusTag = `<span class="status-tag tag-info">ℹ️ PROJECT EXPLANATION</span>`;
  }

  let formattedMsg = formatMarkdown(data.message);

  let codeBox = "";
  if (data.code && data.status === "VERIFIED") {
    codeBox = `
      <div style="margin-top: 10px;">
        <div style="font-size:0.72rem; font-weight:600; color:var(--text-muted); text-transform:uppercase;">Synthesized Python Proof Script:</div>
        <pre class="code-container"><code>${escapeHtml(data.code)}</code></pre>
      </div>
    `;
  }

  let certBox = "";
  if (data.certificate && data.status === "VERIFIED") {
    const cert = data.certificate;
    certBox = `
      <div class="cert-box">
        <div><span>Proof ID:</span> <strong>${cert.proof_id}</strong></div>
        <div><span>SHA-256 Code Seal:</span> <strong>${cert.code_sha256.substring(0, 24)}...</strong></div>
        <div><span>Sandbox Latency:</span> <strong>${cert.execution_time_ms.toFixed(2)} ms (Exit 0)</strong></div>
      </div>
    `;
  }

  div.innerHTML = `
    <div style="margin-bottom: 8px;">${statusTag}</div>
    <div style="line-height: 1.6;">${formattedMsg}</div>
    ${codeBox}
    ${certBox}
  `;

  stream.appendChild(div);
  stream.scrollTop = stream.scrollHeight;
}

function formatMarkdown(text) {
  if (!text) return "";
  let out = escapeHtml(text);
  out = out.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/`([^`]+)`/g, "<code style='background:rgba(0,0,0,0.4); padding:2px 4px; border-radius:4px; color:var(--primary);'>$1</code>");
  out = out.replace(/\n- (.*?)/g, "<br>• $1");
  out = out.replace(/\n/g, "<br>");
  return out;
}

async function run10Benchmarks() {
  alert("Running all 10 evaluation benchmarks... (takes ~5 seconds)");
  try {
    const res = await fetch("/api/benchmark");
    const data = await res.json();
    alert(`Benchmark Evaluation Results:\nTotal Tests: ${data.total}\nPassed: ${data.passed}\nFailed: ${data.failed}\nSuccess Rate: ${(data.passed / data.total * 100).toFixed(1)}%\n\nZero unverified numbers emitted!`);
  } catch (err) {
    alert("Benchmark execution failed: " + err.message);
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
