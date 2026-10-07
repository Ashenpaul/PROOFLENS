import urllib.request
import json

def test():
    # 1. Upload a completely new custom dataset: 'employees.csv'
    sample_csv = """emp_id,name,department,salary,join_year
E101,Alice,Engineering,95000,2021
E102,Bob,Product,105000,2020
E103,Charlie,Engineering,110000,2019
E104,Diana,Marketing,80000,2022
E104,Diana,Marketing,80000,2022
"""
    req_upload = urllib.request.Request(
        'http://127.0.0.1:8080/api/upload',
        data=json.dumps({'filename': 'employees.csv', 'content': sample_csv}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    res_upload = json.loads(urllib.request.urlopen(req_upload).read().decode())
    print("UPLOAD RESULT:", res_upload["success"], "Filename:", res_upload["filename"], "Rows:", res_upload["row_count"], "Columns:", res_upload["columns"])

    # 2. Query the uploaded dataset: 'What is the total salary for employees?'
    req_query = urllib.request.Request(
        'http://127.0.0.1:8080/api/chat',
        data=json.dumps({'message': 'What is the total salary in employees?'}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    res_query = json.loads(urllib.request.urlopen(req_query).read().decode())
    print("QUERY ON UPLOADED DATASET:", res_query["status"], "Answer:", res_query.get("answer"))
    print("PROOF CODE:")
    print(res_query.get("code"))

if __name__ == "__main__":
    test()
