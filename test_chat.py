import urllib.request
import json

def test():
    # 1. Meta question
    req1 = urllib.request.Request(
        'http://127.0.0.1:8080/api/chat',
        data=json.dumps({'message': 'Explain how the sandbox verifier works'}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    res1 = json.loads(urllib.request.urlopen(req1).read().decode())
    print("TEST 1 (Meta):", res1["status"], res1["reply_type"])

    # 2. Analytical query
    req2 = urllib.request.Request(
        'http://127.0.0.1:8080/api/chat',
        data=json.dumps({'message': 'What is the total net revenue in USD?'}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    res2 = json.loads(urllib.request.urlopen(req2).read().decode())
    print("TEST 2 (Analytical):", res2["status"], res2.get("answer"))

    # 3. Trap query
    req3 = urllib.request.Request(
        'http://127.0.0.1:8080/api/chat',
        data=json.dumps({'message': 'What is the total revenue for APAC in 2023?'}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    res3 = json.loads(urllib.request.urlopen(req3).read().decode())
    print("TEST 3 (Trap):", res3["status"], res3.get("trap_type"))

if __name__ == "__main__":
    test()
