import requests
import time

BASE_URL = "http://localhost:8000"  # nếu chạy part 4 tại cổng 8000


def test_suite():
    print("=== 1. Checking Health ===")
    r = requests.get(f"{BASE_URL}/health")
    print(f"Health Status: {r.status_code} - {r.json()}\n")

    print("=== 2. Testing Unauthorized Access (No Token) ===")
    r = requests.post(f"{BASE_URL}/ask", json={"question": "Who are you?"})
    print(f"Status: {r.status_code} (Expected 401)")
    print(f"Detail: {r.json()}\n")

    print("=== 3. Logging in (Get JWT) ===")
    login_data = {"username": "student", "password": "demo123"}
    r = requests.post(f"{BASE_URL}/auth/token", json=login_data)
    token = r.json().get("access_token")
    print(f"Token received: {token[:30]}...\n")

    headers = {"Authorization": f"Bearer {token}"}

    print("=== 4. Testing Authorized Request ===")
    r = requests.post(
        f"{BASE_URL}/ask", json={"question": "What is Docker?"}, headers=headers
    )
    print(f"Status: {r.status_code}")
    print(f"Answer: {r.json().get('answer')}\n")

    print("=== 5. Testing Rate Limit (Spamming 12 requests) ===")
    for i in range(12):
        r = requests.post(
            f"{BASE_URL}/ask", json={"question": f"Spam {i}"}, headers=headers
        )
        print(f"Req {i+1}: Status {r.status_code}")
        if r.status_code == 429:
            print("Successfully triggered Rate Limit (429)!")
            break


if __name__ == "__main__":
    try:
        test_suite()
    except Exception as e:
        print(f"Error: {e}")
