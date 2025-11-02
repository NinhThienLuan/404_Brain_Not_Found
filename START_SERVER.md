# 🚀 Hướng Dẫn Chạy Server

## ✅ Cách 1: Chạy Trực Tiếp (Recommended)

### Bước 1: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 2: Chạy server

```bash
python -m BE.main
```

**Output mong đợi:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Bước 3: Test server

Mở browser: **http://localhost:8000**

Hoặc test bằng Python (terminal mới):
```bash
python test_with_requests.py
```

---

## ✅ Cách 2: Chạy Background (Windows)

### PowerShell:
```powershell
Start-Process python -ArgumentList "-m", "BE.main" -WindowStyle Hidden
```

### Hoặc dùng `start`:
```cmd
start /B python -m BE.main
```

---

## 🐛 Troubleshooting

### Lỗi: `ModuleNotFoundError: No module named 'email_validator'`

**Fix:**
```bash
pip install email-validator
```

Hoặc:
```bash
pip install 'pydantic[email]'
```

### Lỗi: `Port 8000 already in use`

**Fix 1:** Kill process đang dùng port 8000
```powershell
# Tìm process
netstat -ano | findstr :8000

# Kill process (thay <PID> bằng số hiện ra)
taskkill /PID <PID> /F
```

**Fix 2:** Đổi port trong `BE/main.py`:
```python
uvicorn.run(
    "BE.main:app",
    host="0.0.0.0",
    port=8001,  # ← Đổi thành 8001
    reload=True
)
```

### Lỗi: MongoDB connection

**Test connection:**
```bash
python test_connection.py
```

**Nếu thất bại:** Kiểm tra file `.env` có đúng thông tin MongoDB không.

---

## ✅ Verify Server Running

### Test 1: Browser
```
http://localhost:8000/
```

**Expected:**
```json
{
  "status": "OK",
  "message": "Hackathon API đang chạy!",
  "docs": "/docs"
}
```

### Test 2: API Docs
```
http://localhost:8000/docs
```

### Test 3: Python Script
```bash
python test_with_requests.py
```

### Test 4: Postman
Import: `User_API.postman_collection.json`

---

## 🎯 Next Steps

Sau khi server chạy thành công:

1. **Test API với Postman:**
   - Import `User_API.postman_collection.json`
   - Run collection

2. **Test với Python:**
   ```bash
   python test_with_requests.py
   ```

3. **Test với Swagger UI:**
   - http://localhost:8000/docs

---

## 📊 Endpoints Available

- `GET /` - Health check
- `GET /api/users/` - Lấy danh sách users
- `POST /api/users/` - Tạo user mới
- `GET /api/users/{id}` - Lấy user theo ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Xóa user

**Full docs:** http://localhost:8000/docs

---

Happy coding! 🚀

