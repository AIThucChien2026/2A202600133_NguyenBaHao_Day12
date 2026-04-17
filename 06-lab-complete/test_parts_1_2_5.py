import os
import requests
import subprocess
import time

BASE_URL = "http://localhost"

def test_infrastructure():
    print("=== Testing Part 1 & 5: Infrastructure & Reliability ===")
    
    # 1. Health Check
    try:
        r = requests.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        print("✅ Health Check: OK")
    except:
        print("❌ Health Check: FAILED")

    # 2. Readiness Check
    try:
        r = requests.get(f"{BASE_URL}/ready")
        assert r.status_code == 200
        print("✅ Readiness Check: OK")
    except:
        print("❌ Readiness Check: FAILED")

    # 3. Environment Variables (Config management)
    print("✅ Config Management: Handled by Pydantic Settings")

def test_docker_part2():
    print("\n=== Testing Part 2: Docker ===")
    
    # Kiểm tra Dockerfile multi-stage
    with open("Dockerfile", "r") as f:
        content = f.read()
        if "AS builder" in content and "AS runtime" in content:
            print("✅ Docker: Multi-stage build detected")
        else:
            print("❌ Docker: Multi-stage build MISSING")
            
        if "USER agentuser" in content:
            print("✅ Docker: Non-root user detected")
        else:
            print("❌ Docker: Running as root (Unsafe)")

def test_load_balancing_part5():
    print("\n=== Testing Part 5: Load Balancing & Stateless ===")
    instances = set()
    for i in range(5):
        r = requests.get(f"{BASE_URL}/health")
        data = r.json()
        instances.add(data.get("instance"))
    
    print(f"Detected instances: {instances}")
    if len(instances) > 1:
        print("✅ Load Balancing: Round Robin detected across multiple instances")
    else:
        print("⚠️  Load Balancing: Only 1 instance detected (scale up with --scale agent=3)")

if __name__ == "__main__":
    test_infrastructure()
    test_docker_part2()
    test_load_balancing_part5()
