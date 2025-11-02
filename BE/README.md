# User CRUD API

API CRUD hoàn chỉnh cho User với MongoDB.

## 📦 Cài đặt

```bash
pip install -r ../requirements.txt
```

## 🚀 Chạy Server

```bash
# Từ thư mục gốc project
python -m BE.main

# Hoặc
cd BE
python main.py
```

Server sẽ chạy tại: http://localhost:8000

## 📚 API Documentation

Sau khi chạy server, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 API Endpoints

### 1. **Tạo User Mới** - `POST /api/users/`

**Request Body:**
```json
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

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nguyễn Văn A","email":"a@example.com"}'
```

---

### 2. **Lấy User Theo ID** - `GET /api/users/{user_id}`

**Response:** `200 OK`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A",
  "email": "a@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/users/6906ae5b2484813d2b42c6db"
```

---

### 3. **Lấy Danh Sách Users** - `GET /api/users/`

**Query Parameters:**
- `page` (optional): Số trang, mặc định = 1
- `page_size` (optional): Số items/trang, mặc định = 10, max = 100

**Response:** `200 OK`
```json
{
  "users": [
    {
      "_id": "6906ae5b2484813d2b42c6db",
      "name": "Nguyễn Văn A",
      "email": "a@example.com",
      "created_at": "2025-11-02T01:05:31.153Z"
    },
    {
      "_id": "6906ae692484813d2b42c6dc",
      "name": "Trần Thị B",
      "email": "b@example.com",
      "created_at": "2025-11-02T01:05:45.823Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/users/?page=1&page_size=10"
```

---

### 4. **Lấy User Theo Email** - `GET /api/users/email/{email}`

**Response:** `200 OK`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A",
  "email": "a@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/users/email/a@example.com"
```

---

### 5. **Update User** - `PUT /api/users/{user_id}`

**Request Body:** (tất cả fields đều optional)
```json
{
  "name": "Nguyễn Văn C",
  "email": "c@example.com"
}
```

**Response:** `200 OK`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn C",
  "email": "c@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/users/6906ae5b2484813d2b42c6db" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nguyễn Văn C","email":"c@example.com"}'
```

---

### 6. **Partial Update User** - `PATCH /api/users/{user_id}`

Giống PUT nhưng semantic khác (partial update).

---

### 7. **Xóa User** - `DELETE /api/users/{user_id}`

**Response:** `200 OK`
```json
{
  "message": "Đã xóa user với ID '6906ae5b2484813d2b42c6db' thành công"
}
```

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/users/6906ae5b2484813d2b42c6db"
```

---

## 🧪 Test API với Python

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Tạo user mới
response = requests.post(f"{BASE_URL}/api/users/", json={
    "name": "Test User",
    "email": "test@example.com"
})
user = response.json()
print(f"Created: {user}")

user_id = user["_id"]

# 2. Lấy user
response = requests.get(f"{BASE_URL}/api/users/{user_id}")
print(f"Get: {response.json()}")

# 3. Update user
response = requests.put(f"{BASE_URL}/api/users/{user_id}", json={
    "name": "Updated Name"
})
print(f"Updated: {response.json()}")

# 4. Lấy danh sách users
response = requests.get(f"{BASE_URL}/api/users/?page=1&page_size=10")
print(f"List: {response.json()}")

# 5. Xóa user
response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
print(f"Deleted: {response.json()}")
```

## 🏗️ Cấu trúc Code

```
BE/
├── models/
│   └── user_model.py          # Pydantic models (optional, dùng nếu cần)
├── repository/
│   └── user_repo.py           # CRUD operations với MongoDB
├── service/
│   └── user_service.py        # Business logic
├── controller/
│   └── user_controller.py     # API endpoints (FastAPI routes)
└── main.py                    # FastAPI app
```

### Layer Architecture:

```
Controller (API) 
    ↓ 
Service (Business Logic) 
    ↓ 
Repository (Database Operations)
```

## ✨ Features

✅ **CRUD đầy đủ**: Create, Read, Update, Delete
✅ **Pagination**: Hỗ trợ phân trang cho danh sách users
✅ **Validation**: Email validation, unique email constraint
✅ **Error Handling**: Xử lý lỗi chi tiết với HTTP status codes
✅ **Auto Documentation**: Swagger UI và ReDoc
✅ **Type Safety**: Sử dụng Pydantic models
✅ **Clean Architecture**: Tách biệt Controller - Service - Repository

## 🔐 Environment Variables

Tạo file `.env` trong thư mục gốc:

```env
MONGO_USERNAME=mongo
MONGO_PASSWORD=your_password
MONGO_HOST=shortline.proxy.rlwy.net
MONGO_PORT=21101
MONGO_DATABASE=basic-hackathon
```

## 📝 Response Codes

- `200 OK`: Request thành công
- `201 Created`: Tạo mới thành công
- `400 Bad Request`: Dữ liệu không hợp lệ
- `404 Not Found`: Không tìm thấy resource
- `500 Internal Server Error`: Lỗi server

## 🐛 Troubleshooting

### Lỗi kết nối MongoDB:
```bash
python test_connection.py  # Chạy test connection trước
```

### Port 8000 đã được sử dụng:
Thay đổi port trong `main.py`:
```python
uvicorn.run(..., port=8001)
```

## 🎯 Next Steps

- [ ] Add authentication (JWT)
- [ ] Add input sanitization
- [ ] Add rate limiting
- [ ] Add logging
- [ ] Add tests (pytest)
- [ ] Add Docker support

