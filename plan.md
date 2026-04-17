# 📋 Lộ trình Thực hành: Đưa AI Agent lên Production (Cloud)

> **Project:** Day 12 — Hạ tầng Cloud & Triển khai (Deployment)  
> **Mục tiêu:** Biến một AI Agent chạy trên máy cá nhân thành một dịch vụ Cloud chuyên nghiệp, bảo mật và có khả năng mở rộng.

---

## 🎯 Mục tiêu bài Lab
- Hiểu sự khác biệt giữa **Dev (Máy cá nhân)** và **Production (Môi trường thật)** qua nguyên tắc 12-Factor App.
- Làm chủ **Docker** (Tối ưu hóa hình ảnh container, chạy nhiều dịch vụ với Docker Compose).
- Triển khai lên các nền tảng **Cloud** (Railway, Render, Cloud Run).
- Bảo mật **API** (Xác thực JWT, Giới hạn lượt gọi - Rate Limiting, Kiểm soát chi phí - Cost Guard).
- Đảm bảo **Độ tin cậy & Mở rộng** (Kiểm tra sức khỏe - Health checks, Thiết kế không lưu trạng thái - Stateless).
- Xây dựng một **Agent hoàn chỉnh** sẵn sàng cho người dùng thật.

---

## 🛠 Yêu cầu chuẩn bị
Hãy đảm bảo máy bạn đã cài đặt:
- [ ] **Python 3.11+**
- [ ] **Docker & Docker Compose** (Công cụ đóng gói ứng dụng)
- [ ] **Git** (Quản lý mã nguồn)
- [ ] **Node.js/npm** (Để cài Railway CLI)
- [ ] **Postman hoặc cURL** (Để kiểm tra API)

---

## 🗺️ Lộ trình & Thời gian (Dự kiến 3-4 giờ)

| Giai đoạn | Thời gian | Nội dung chính |
| :--- | :--- | :--- |
| **Phần 1** | 30 phút | Localhost vs. Production (Sửa lỗi bảo mật & Cấu hình) |
| **Phần 2** | 45 phút | Docker hóa ứng dụng (Đóng gói & Tối ưu dung lượng) |
| **Phần 3** | 45 phút | Triển khai lên Cloud (Đưa app lên Railway/Render) |
| **Phần 4** | 40 phút | Bảo mật API (Khóa API, Giới hạn lượt gọi, Ngân sách) |
| **Phần 5** | 40 phút | Khả năng mở rộng (Chạy nhiều máy chủ, Kiểm tra lỗi) |
| **Phần 6** | 60 phút | **Dự án cuối khóa: AI Agent chuẩn Production** |

---

## 🚀 Hướng dẫn thực hiện chi tiết

### Phần 1: Localhost vs. Production
- **Mục tiêu:** Tìm và sửa các lỗi "chạy được trên máy tôi nhưng lỗi trên server".
- **Công việc:**
    1. Đọc file `01.../develop/app.py` để tìm các lỗi: lộ mã bí mật (API Key), cổng (port) cố định.
    2. Sử dụng file `.env` để quản lý cấu hình thay vì viết trực tiếp vào mã nguồn.
    3. Thay thế `print()` bằng logging chuyên nghiệp (dạng JSON) để dễ theo dõi lỗi trên Cloud.

### Phần 2: Docker hóa ứng dụng
- **Mục tiêu:** Đóng gói ứng dụng để chạy ở đâu cũng giống nhau.
- **Công việc:**
    1. Viết `Dockerfile` cơ bản để tạo "thùng chứa" ứng dụng.
    2. Sử dụng **Multi-stage build** để giảm dung lượng file xuống dưới 200MB (giúp deploy nhanh hơn).
    3. Dùng `docker-compose.yml` để chạy Agent cùng với database Redis.

### Phần 3: Triển khai lên Cloud
- **Mục tiêu:** Lấy đường dẫn (URL) công khai để ai cũng truy cập được.
- **Công việc:**
    1. **Railway:** Dùng lệnh `railway up` để đẩy code lên.
    2. **Render:** Kết nối với GitHub và cấu hình qua file `render.yaml`.
    3. Kiểm tra xem URL công khai đã hoạt động chưa qua trình duyệt.

### Phần 4: Bảo mật API (Bảo vệ "ví tiền" của bạn)
- **Mục tiêu:** Tránh bị người lạ dùng chùa làm tốn tiền API OpenAI.
- **Công việc:**
    1. Thêm xác thực **X-API-Key** vào tiêu đề (header) của request.
    2. Cấu hình **Rate Limiting** (ví dụ: tối đa 10 câu hỏi/phút) để tránh bị tấn công spam.
    3. Cài đặt **Cost Guard** để tự động ngắt kết nối nếu người dùng tiêu quá 10$/tháng.

### Phần 5: Khả năng mở rộng & Độ tin cậy
- **Mục tiêu:** Hệ thống vẫn chạy tốt khi có hàng ngàn người dùng hoặc khi 1 máy chủ bị lỗi.
- **Công việc:**
    1. Thêm endpoint `/health` (để Cloud biết app còn sống) và `/ready` (để biết app đã sẵn sàng nhận khách).
    2. Xử lý **Graceful Shutdown**: Đảm bảo app không bị tắt đột ngột khi đang xử lý câu hỏi.
    3. Chuyển sang thiết kế **Stateless**: Lưu lịch sử chat vào Redis thay vì lưu trong bộ nhớ máy (RAM).

### Phần 6: Dự án cuối khóa (Thử thách thực tế)
- **Yêu cầu:** Xây dựng Agent hoàn chỉnh tại thư mục `06-lab-complete`.
- **Tiêu chí chấm điểm:**
    - [ ] Có Dockerfile tối ưu.
    - [ ] Cấu hình hoàn toàn qua biến môi trường (Environment Variables).
    - [ ] Có đầy đủ Bảo mật + Giới hạn lượt gọi.
    - [ ] Có cơ chế kiểm tra sức khỏe (Health checks).
    - [ ] Chạy lệnh `python check_production_ready.py` đạt kết quả 100%.

---

## 💡 Các lệnh quan trọng cần nhớ

### Docker (Đóng gói)
```bash
docker build -t my-agent .          # Tạo image
docker compose up -d --build       # Chạy hệ thống ở chế độ chạy ngầm
```

### Triển khai (Railway)
```bash
railway login                      # Đăng nhập
railway up                         # Đẩy code lên cloud
railway domain                     # Lấy địa chỉ URL của app
```

### Kiểm tra API (cURL)
```bash
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: secret-cua-ban" \
  -H "Content-Type: application/json" \
  -d '{"question": "Xin chào!"}'
```

---

## ✅ Danh sách kiểm tra hoàn thành (Checklist)
- [ ] Agent trả lời đúng câu hỏi qua API.
- [ ] Không có API Key nào bị viết lộ ra trong code.
- [ ] Docker image gọn nhẹ, không chứa file rác.
- [ ] API trả về lỗi 401 nếu sai key, 429 nếu dùng quá nhanh.
- [ ] Có đường dẫn URL công khai và đã được bảo mật.

---

## 🆘 Hỗ trợ khi gặp lỗi
- **Lỗi cổng (Port) đã bị dùng?** Dùng lệnh `lsof -i :8000` để tìm và tắt tiến trình cũ.
- **App không kết nối được Redis?** Kiểm tra xem tên service trong `docker-compose.yml` có khớp với `REDIS_URL` không.
- **Lỗi trên Cloud?** Dùng `railway logs` hoặc xem tab Logs trên dashboard của Render.

---
*AICB-P1 · VinUniversity 2026 — Chúc bạn triển khai thành công!*
