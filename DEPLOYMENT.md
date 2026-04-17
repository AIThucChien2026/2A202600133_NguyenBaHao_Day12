# Deployment Information

## Public URL
https://student-agent-deployment.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://student-agent-deployment.railway.app/health
# Kết quả mong đợi: {"status": "ok"}
```

### API Test (Yêu cầu xác thực)
```bash
curl -X POST https://student-agent-deployment.railway.app/ask \
  -H "X-API-Key: my-super-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Các biến môi trường đã thiết lập
- PORT: 8000
- AGENT_API_KEY: my-super-secret-key

## Ảnh chụp màn hình
- [ ] Ảnh chụp Dashboard Railway
- [ ] Ảnh chụp dịch vụ đang hoạt động
- [ ] Ảnh chụp kết quả kiểm tra
