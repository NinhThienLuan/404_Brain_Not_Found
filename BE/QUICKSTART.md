# Quick Start Guide - FastAPI

## Cài đặt nhanh

### 1. Cài đặt dependencies
```bash
cd BE

# Sử dụng python -m pip thay vì pip trực tiếp
python -m pip install -r requirements.txt

# Hoặc nếu có pip trong PATH:
pip install -r requirements.txt
```

### 2. Tạo file .env
```bash
# Copy từ template
copy .env.example .env

# Hoặc tạo thủ công với nội dung:
GEMINI_API_KEY=your_api_key_here
APP_HOST=localhost
APP_PORT=8000
DEBUG=True
APP_NAME=AI Agent - Code Generation & Review
PREFIX_API=/api
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Lấy Gemini API Key
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập Google Account
3. Click "Create API Key"
4. Copy key và paste vào `.env`

### 4. Chạy ứng dụng

#### Cách 1: Chạy trực tiếp với Python
```bash
python app.py
```

#### Cách 2: Chạy với Uvicorn (recommended)
```bash
# Development mode với auto-reload
uvicorn app:app --reload --host localhost --port 8000

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: **http://localhost:8000**

### 5. Truy cập API Documentation
FastAPI tự động tạo interactive API docs:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Test API 

### Cách 1: Sử dụng Swagger UI (Dễ nhất)
1. Mở trình duyệt: http://localhost:8000/api/docs
2. Click vào endpoint muốn test
3. Click "Try it out"
4. Nhập data và click "Execute"

### Cách 2: Sử dụng curl

#### Test 1: Health Check
```bash
curl http://localhost:8000/api/ai/health
```

#### Test 2: Generate Code
```bash
curl -X POST http://localhost:8000/api/ai/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Create a Python function to reverse a string\",\"language\":\"python\"}"
```

#### Test 3: Review Code
```bash
curl -X POST http://localhost:8000/api/ai/review ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"def add(a,b): return a+b\",\"language\":\"python\",\"review_type\":\"general\"}"
```

### Cách 3: Sử dụng Python requests
```python
import requests

# Generate Code
response = requests.post('http://localhost:8000/api/ai/generate', json={
    "prompt": "Create a function to calculate fibonacci",
    "language": "python"
})
print(response.json())

# Review Code
response = requests.post('http://localhost:8000/api/ai/review', json={
    "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
    "language": "python",
    "review_type": "performance"
})
print(response.json())
```

## Troubleshooting

### Lỗi: GEMINI_API_KEY not found
- Kiểm tra file `.env` đã tồn tại
- Đảm bảo có dòng `GEMINI_API_KEY=...` trong `.env`
- API key phải hợp lệ

### Lỗi: pip not found
Sử dụng `python -m pip` thay vì `pip`:
```bash
python -m pip install -r requirements.txt
```

### Lỗi: Import không tìm thấy
```bash
# Cài đặt lại tất cả dependencies
python -m pip install --upgrade -r requirements.txt
```

### Lỗi: Port đã được sử dụng
Thay đổi `APP_PORT` trong file `.env`:
```
APP_PORT=8001
```

### Lỗi: ModuleNotFoundError
Đảm bảo bạn đang chạy từ thư mục `BE`:
```bash
cd D:\GitHub\404_Brain_Not_Found\BE
python app.py
```

## Performance Tips

### 1. Chạy với nhiều workers (Production)
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Enable access logs
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --access-log
```

### 3. Set log level
```bash
uvicorn app:app --log-level debug
```
