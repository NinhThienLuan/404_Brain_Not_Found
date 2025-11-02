# 🚀 Quick Start - User CRUD API

## 📦 Bước 1: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Bước 2: Chạy Server

```bash
python -m BE.main
```

Server sẽ chạy tại: **http://localhost:8000**

## 📖 Bước 3: Xem API Documentation

Mở trình duyệt và truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Bước 4: Test API

### Option 1: Test bằng script Python

```bash
# Chạy server trước (terminal 1)
python -m BE.main

# Chạy test script (terminal 2)
python test_user_api.py
```

### Option 2: Test bằng cURL

```bash
# Tạo user mới
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nguyễn Văn A","email":"a@example.com"}'

# Lấy danh sách users
curl "http://localhost:8000/api/users/"
```

### Option 3: Test bằng Swagger UI

1. Mở http://localhost:8000/docs
2. Click vào endpoint muốn test
3. Click "Try it out"
4. Nhập data và click "Execute"

## 🎯 API Endpoints Chính

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/users/` | Tạo user mới |
| GET | `/api/users/{user_id}` | Lấy user theo ID |
| GET | `/api/users/` | Lấy danh sách users (có pagination) |
| GET | `/api/users/email/{email}` | Lấy user theo email |
| PUT | `/api/users/{user_id}` | Update user |
| PATCH | `/api/users/{user_id}` | Partial update user |
| DELETE | `/api/users/{user_id}` | Xóa user |

## 📝 Ví dụ Request/Response

### Tạo User Mới

**Request:**
```json
POST /api/users/
{
  "name": "Nguyễn Văn A",
  "email": "a@example.com"
}
```

**Response:** `201 Created`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A",
  "email": "a@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

### Lấy Danh Sách Users

**Request:**
```
GET /api/users/?page=1&page_size=10
```

**Response:** `200 OK`
```json
{
  "users": [
    {
      "_id": "6906ae5b2484813d2b42c6db",
      "name": "Nguyễn Văn A",
      "email": "a@example.com",
      "created_at": "2025-11-02T01:05:31.153Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

## 🏗️ Cấu trúc Project

```
BE/
├── models/          # Pydantic models
├── repository/      # Database operations (CRUD)
├── service/         # Business logic
├── controller/      # API endpoints
└── main.py         # FastAPI app

test_user_api.py    # Test script
test_connection.py  # Test MongoDB connection
```

## ⚙️ Configuration

File `.env` (đã có sẵn):
```env
MONGO_USERNAME=mongo
MONGO_PASSWORD=OtfagZQFKuslkxmpTCZTlvctRGsQBLnk
MONGO_HOST=shortline.proxy.rlwy.net
MONGO_PORT=21101
MONGO_DATABASE=basic-hackathon
```

## 🔧 Troubleshooting

### Lỗi "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### Lỗi kết nối MongoDB
```bash
python test_connection.py  # Test connection trước
```

### Port 8000 đã được sử dụng
Thay đổi port trong `BE/main.py`:
```python
uvicorn.run(..., port=8001)
```

## ✨ Features

✅ CRUD đầy đủ (Create, Read, Update, Delete)  
✅ Pagination cho danh sách users  
✅ Email validation  
✅ Unique email constraint  
✅ Auto-generated API documentation  
✅ Error handling với HTTP status codes  
✅ Clean architecture (Controller → Service → Repository)

## 📚 Documentation Chi Tiết

Xem file `BE/README.md` để biết thêm chi tiết về:
- API endpoints đầy đủ
- Response codes
- Error handling
- Architecture
- Advanced features

Chúc bạn code vui vẻ! 🎉

