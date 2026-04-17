import requests
import json

url = "https://railway-service-production-88d6.up.railway.app/ask"
headers = {
    "X-API-Key": "my-secret-key",
    "Content-Type": "application/json"
}
payload = {
    "question": "Thủ đô của Việt Nam là gì?"
}

try:
    print(f"Gửi câu hỏi: {payload['question']}")
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("-" * 30)
        print(f"Model: {result.get('model')}")
        print(f"Answer: {result.get('answer')}")
        print("-" * 30)
    else:
        print(f"Error Detail: {response.text}")
except Exception as e:
    print(f"Lỗi kết nối: {str(e)}")
