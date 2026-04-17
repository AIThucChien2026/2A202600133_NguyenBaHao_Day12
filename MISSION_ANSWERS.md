# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Các Anti-patterns đã phát hiện
1. **Hardcoded Secrets:** API key và thông tin database được để trực tiếp trong code, gây rủi ro lộ lọt thông tin nhạy cảm khi đẩy lên repository.
2. **Thiếu cơ chế quản lý cấu hình:** Không có sự tách biệt giữa cấu hình môi trường phát triển và môi trường thực tế (ví dụ: cờ DEBUG, cổng kết nối).
3. **Sử dụng lệnh print():** Việc dùng `print()` để log khiến hệ thống khó theo dõi, thiếu tính quan sát (observability) và không thể phân tích log theo cấu trúc trong môi trường sản xuất.
4. **Không có Health Check:** Ứng dụng không cung cấp endpoint cho phép các nền tảng (như Docker/Cloud) kiểm tra tình trạng sức khỏe (liveness), dẫn đến việc platform không thể tự động xử lý khi ứng dụng gặp sự cố.
5. **Cấu hình cứng (Rigid Configuration):** Cổng kết nối và địa chỉ host được cố định, làm giảm tính linh hoạt khi triển khai trên các hạ tầng cloud khác nhau.

### Exercise 1.3: Bảng so sánh
| Đặc điểm | Môi trường phát triển | Môi trường sản xuất | Tại sao quan trọng? |
|---------|---------|------------|----------------|
| Cấu hình | Hardcode trong code | Biến môi trường (Env Vars) | Đảm bảo bảo mật và tính di động của mã nguồn. |
| Health check | Không có | Có endpoint `/health` | Giúp Orchestrator giám sát trạng thái ứng dụng. |
| Ghi log | Dùng `print()` | Log theo cấu trúc (JSON) | Phục vụ truy vết, phân tích lỗi và giám sát hệ thống. |
| Ngắt kết nối | Đột ngột | Graceful Shutdown | Bảo toàn dữ liệu, hoàn tất các yêu cầu đang xử lý. |

## Part 2: Docker

### Exercise 2.1: Các câu hỏi về Dockerfile
1. **Base image:** Sử dụng `python:3.11` (phiên bản đầy đủ).
2. **Working directory:** Thư mục `/app`.
3. **Tại sao copy requirements trước?** Để tận dụng cơ chế Layer Caching của Docker, giúp việc build lại nhanh hơn khi chỉ thay đổi code mà không thay đổi dependencies.
4. **Sự khác biệt giữa CMD và ENTRYPOINT:** `CMD` cung cấp lệnh mặc định có thể dễ dàng ghi đè, trong khi `ENTRYPOINT` xác định ứng dụng chính và khó bị ghi đè hơn.

### Exercise 2.3: Multi-stage build
- **Giai đoạn 1 (Builder):** Cài đặt các công cụ biên dịch (như gcc) và các thư viện cần thiết vào một môi trường tạm thời.
- **Giai đoạn 2 (Runtime):** Chỉ sao chép các gói thư viện đã cài đặt và mã nguồn từ giai đoạn trước, tạo ra image gọn nhẹ và bảo mật hơn do không chứa các công cụ build.

## Part 3: Cloud Deployment

### Exercise 3.1: Triển khai trên Railway
- **Trạng thái:** Đã triển khai thành công.
- **Quy trình:** Tôi đã sử dụng Railway CLI (`railway init` rồi `railway up`) và thiết lập các biến môi trường cần thiết (`PORT`, `AGENT_API_KEY`) thông qua CLI để ứng dụng hoạt động ổn định trên nền tảng cloud.
