#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:**  Nguyen Ba hao
> 
> **Student ID:** 2A202600133
> 
> **Date:** 18/04/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

```markdown
# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets:** API key và thông tin database được để trực tiếp trong code, gây rủi ro lộ lọt thông tin nhạy cảm khi đẩy lên repository.
2. **Thiếu cơ chế quản lý cấu hình:** Không có sự tách biệt giữa cấu hình môi trường phát triển và môi trường thực tế (ví dụ: cờ DEBUG, cổng kết nối).
3. **Sử dụng lệnh print():** Việc dùng `print()` để log khiến hệ thống khó theo dõi, thiếu tính quan sát (observability) và không thể phân tích log theo cấu trúc trong môi trường sản xuất.
4. **Không có Health Check:** Ứng dụng không cung cấp endpoint cho phép các nền tảng (như Docker/Cloud) kiểm tra tình trạng sức khỏe (liveness), dẫn đến việc platform không thể tự động xử lý khi ứng dụng gặp sự cố.
5. **Cấu hình cứng (Rigid Configuration):** Cổng kết nối và địa chỉ host được cố định, làm giảm tính linh hoạt khi triển khai trên các hạ tầng cloud khác nhau.

### Exercise 1.3:Comparison tabl
| Đặc điểm | Môi trường phát triển | Môi trường sản xuất | Tại sao quan trọng? |
|---------|---------|------------|----------------|
| Cấu hình | Hardcode trong code | Biến môi trường (Env Vars) | Đảm bảo bảo mật và tính di động của mã nguồn. |
| Health check | Không có | Có endpoint `/health` | Giúp Orchestrator giám sát trạng thái ứng dụng. |
| Ghi log | Dùng `print()` | Log theo cấu trúc (JSON) | Phục vụ truy vết, phân tích lỗi và giám sát hệ thống. |
| Ngắt kết nối | Đột ngột | Graceful Shutdown | Bảo toàn dữ liệu, hoàn tất các yêu cầu đang xử lý. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image:** Sử dụng `python:3.11'.
2. **Working directory:** Thư mục `/app`.
3. **Tại sao copy requirements trước?** Để tận dụng cơ chế Layer Caching của Docker, giúp việc build lại nhanh hơn khi chỉ thay đổi code mà không thay đổi dependencies.
4. **Sự khác biệt giữa CMD và ENTRYPOINT:** `CMD` cung cấp lệnh mặc định có thể dễ dàng ghi đè, trong khi `ENTRYPOINT` xác định ứng dụng chính và khó bị ghi đè hơn.

### Exercise 2.3: Image size comparison
- Develop: 1.66 GB 
- Production: 238MB
- Difference: 85.66%


## Part 3: Cloud Deployment

### Exercise 3.1: Render deployment
- URL: https://ai-agent-pp5g.onrender.com
- Screenshot: [Link to screenshot in repo]

## Part 4: API Security

### Exercise 4.1-4.3: Test results


#### 1. Kiểm tra Authentication (API Key)
- **Lệnh thực hiện:** 
  `Invoke-RestMethod -Uri "http://localhost:8000/ask?question=Hello" -Method Post -Headers @{"X-API-Key" = "demo-key-change-in-production"}`
- **Kết quả:** 
  - Không có key: Trả về **401 Unauthorized**.
  - Có key hợp lệ: Trả về **200 OK** kèm câu trả lời từ AI Agent.

#### 2. Kiểm tra JWT Authentication
- **Lệnh thực hiện:** 
  `$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/token" -Method Post -ContentType "application/json" -Body '{"username": "student", "password": "demo123"}'`
  `$token = $response.access_token`
  `Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -Headers @{Authorization = "Bearer $token"} -Body '{"question": "What is Docker?"}'`
- **Kết quả:** Hệ thống trả về `access_token` hợp lệ. Khi gọi API với header `Authorization: Bearer <token>`, nhận được phản hồi **200 OK** với nội dung:
  ```json
  {
      "question": "What is Docker?",
      "answer": "Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!",
      "usage": { "requests_remaining": 9, "budget_remaining_usd": 1.9E-05 }
  }
  ```

#### 3. Kiểm tra Rate Limiting (Giới hạn 10 request/phút)
- **Lệnh thực hiện:** 
  `for ($i = 1; $i -le 20; $i++) { Invoke-WebRequest -Uri "http://localhost:8000/ask" -Method Post -Headers @{Authorization = "Bearer $token"} -Body '{"question": "Test"}' -UseBasicParsing }`
- **Kết quả:** 
  - 10 yêu cầu đầu tiên: Trả về **200 OK**.
  - Các yêu cầu từ 11 đến 20: Trả về **429 Too Many Requests**. (Đúng theo cấu hình của tài khoản `student`).

#### 4. Kiểm tra Cost Guard
- **Kết quả:** Khi giả lập sử dụng vượt ngưỡng ngân sách ($1.0/ngày), hệ thống đã kích hoạt cơ chế bảo vệ và trả về mã lỗi **402 Payment Required** theo đúng thiết kế.

---
#### 5. Xác nhận toàn diện bằng Script tự động
- **Tệp thực hiện:** `test_security_suite.py`
- **Nội dung kiểm tra:** Tự động hóa việc kiểm tra Health, Unauthorized (401), JWT Login, Authorized (200) và Rate Limit (429).
- **Kết quả:** Script chạy thành công 100%, xác nhận tất cả các lớp bảo mật (Auth, Rate Limit, Cost Guard) hoạt động đồng bộ và chính xác.
  ```text
  === 1. Checking Health ===
  Health Status: 200 - OK
  === 2. Testing Unauthorized Access ===
  Status: 401 (Expected)
  === 3. Logging in (Get JWT) ===
  Token received: eyJhbGciOiJIUzI1Ni...
  === 4. Testing Authorized Request ===
  Status: 200 - Answer: Container là cách đóng gói app...
  === 5. Testing Rate Limit ===
  Req 10: Status 429 - Successfully triggered Rate Limit!
  ```



### Exercise 4.4: Cost guard implementation
Cơ chế Cost Guard được triển khai bằng cách:
1. **Tính toán chi phí:** Dựa trên số lượng token đầu vào (question) và đầu ra (answer). Mỗi 1000 tokens được quy đổi ra USD theo đơn giá cấu hình.
2. **Kiểm tra trước khi gọi (Pre-check):** Trước mỗi yêu cầu `/ask`, hệ thống kiểm tra tổng chi phí đã dùng trong ngày của user đó trong Redis. Nếu vượt quá `DAILY_BUDGET_USD` (mặc định $1.0), hệ thống trả về mã lỗi **402 Payment Required**.
3. **Ghi nhận sau khi gọi (Post-record):** Sau khi nhận phản hồi từ LLM, hệ thống cập nhật (increment) chi phí vào Redis với key có thời gian hết hạn (TTL) là 24 giờ để tự động reset theo ngày.

## Part 6: Final Project - Production Ready AI Agent

### 1. Kết quả kiểm thử toàn diện
Tôi đã xây dựng dự án hoàn chỉnh trong thư mục `my-production-agent` và chạy script `check_production_ready.py`.
- **Kết quả:** **20/20 checks passed (100%)** ✅.
- **Tích hợp LLM thật:** Đã tích hợp thành công **Google Gemini/Gemma API** (model `gemini-1.5-flash`).
- **Kết quả gọi API thực tế:**
  - `POST /ask` với câu hỏi "Thủ đô của Việt Nam là gì?"
  - **Trả lời từ AI:** "Thủ đô của Việt Nam là **Hà Nội**."
- **Minh chứng hệ thống:**
  - **Stateless:** Sử dụng Redis cho cả Rate Limit (Sliding Window) và Cost Guard.
  - **Scalability:** Đã triển khai Nginx Load Balancer phân phối cho 3 Agent instances.
  - **Reliability:** Đầy đủ `/health`, `/ready` và cơ chế Graceful Shutdown.
  - **Docker:** Dockerfile tối ưu (multi-stage), chạy với user non-root.

### 2. Cấu trúc Source Code
Hệ thống tuân thủ cấu trúc chuẩn:
- `app/main.py`: Logic chính, tích hợp Real LLM và Redis History.
- `app/config.py`: Quản lý cấu hình qua .env và Pydantic Settings.
- `app/auth.py`, `app/rate_limiter.py`, `app/cost_guard.py`: Các module bảo mật.
- `Dockerfile` & `docker-compose.yml`: Đóng gói và điều phối 3 replica.

---

### Exercise 5.1-5.5: Implementation notes

- **Phần Develop (Liveness & Readiness):**
  - Đã kiểm thử thành công bằng lệnh: `Invoke-RestMethod -Uri "http://localhost:8000/health"` tương tự với /ready
  - **Bằng chứng thực tế (Raw Response):**
    ```json
    {
        "status": "ok",
        "uptime_seconds": 15.7,
        "checks": { "memory": { "status": "ok", "used_percent": 83.2 } }
    }
    ```
  - `/ready` endpoint trả về `{"ready": true, "in_flight_requests": 1}`.

- **Phần Production (Stateless & Scaling):**
  - Đã scale hệ thống lên **3 instances** và chạy `test_stateless.py`.
  - **Bằng chứng thực tế (Log từ script test_stateless.py):**
    ```text
    Session ID: 4fe053fc-0229-45db-9ad7-0abbaf8365ff
    Request 1: [instance-5bd45f] - Q: What is Docker?
    Request 2: [instance-1857aa] - Q: Why do we need containers?
    Request 3: [instance-953aab] - Q: What is Kubernetes?
    Request 4: [instance-5bd45f] - Q: How does load balancing work?
    Request 5: [instance-1857aa] - Q: What is Redis used for?

    Total requests: 5
    Instances used: {'instance-953aab', 'instance-5bd45f', 'instance-1857aa'}
    ✅ All requests served despite different instances!
    ✅ Session history preserved across all instances via Redis!
    ```
  - **Phân tích:** Load Balancer (Nginx) đã phân phối request qua cả 3 instance. Dữ liệu Session vẫn nhất quán vì được lưu tại Redis, không bị mất khi chuyển instance.
```

---

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:

```
your-repo/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── auth.py              # Authentication
│   ├── rate_limiter.py      # Rate limiting
│   └── cost_guard.py        # Cost protection
├── utils/
│   └── mock_llm.py          # Mock LLM (provided)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker ignore
├── railway.toml             # Railway config (or render.yaml)
└── README.md                # Setup instructions
```

**Requirements:**
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets

---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://your-agent.railway.app

## Platform
Railway / Render / Cloud Run

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
```

##  Pre-Submission Checklist

- [ ] Repository is public (or instructor has access)
- [ ] `MISSION_ANSWERS.md` completed with all exercises
- [ ] `DEPLOYMENT.md` has working public URL
- [ ] All source code in `app/` directory
- [ ] `README.md` has clear setup instructions
- [ ] No `.env` file committed (only `.env.example`)
- [ ] No hardcoded secrets in code
- [ ] Public URL is accessible and working
- [ ] Screenshots included in `screenshots/` folder
- [ ] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/your-username/day12-agent-deployment
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
