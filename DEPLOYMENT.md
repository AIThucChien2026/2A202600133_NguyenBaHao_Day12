# Deployment Information

## Public URL
https://railway-service-production-88d6.up.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://railway-service-production-88d6.up.railway.app/health
# Kết quả mong đợi: {"status": "ok"}
```

### API Test (Yêu cầu xác thực)
```bash
curl -X POST https://railway-service-production-88d6.up.railway.app/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Các biến môi trường đã thiết lập
- PORT
- REDIS_URL
- AGENT_API_KEY
- GOOGLE_API_KEY
- LLM_MODEL

## Ảnh chụp màn hình
- [x] Ảnh chụp Dashboard Railway: [dashboard.png](screenshot/dashboard.png)
- [x] Ảnh chụp dịch vụ đang hoạt động: [runing.png](screenshot/runing.png)
- [x] Ảnh chụp kết quả kiểm tra: [testing.png](screenshot/testing.png)
