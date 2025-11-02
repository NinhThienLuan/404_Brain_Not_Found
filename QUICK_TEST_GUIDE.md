# ⚡ Quick Test Guide - 3 Cách Test API

## 🚀 Bước 1: Start Server

```bash
python -m BE.main
```

Server: **http://localhost:8000**

---

## 🎯 3 Cách Test API

### 1️⃣ **Postman (Recommended)** ⭐

**Bước 1:** Import collection
```
File: User_API.postman_collection.json
```

**Bước 2:** Chạy requests
- Tất cả endpoints có sẵn
- Auto-save `user_id` và `user_email`
- Đầy đủ test cases

**Chi tiết:** Xem `POSTMAN_GUIDE.md`

---

### 2️⃣ **Python Script**

```bash
python test_with_requests.py
```

**Output:**
```
🧪 BẮT ĐẦU TEST USER API
====================================
✓ PASS  Health Check
✓ PASS  Tạo User
✓ PASS  Lấy Danh Sách Users
...
🎉 TẤT CẢ TESTS ĐỀU PASS!
```

---

### 3️⃣ **Swagger UI (Built-in)**

1. Mở: **http://localhost:8000/docs**
2. Click endpoint → **Try it out**
3. Nhập data → **Execute**

---

## 📋 API Endpoints Chính

### ✅ Lấy Danh Sách Users
```http
GET /api/users/?page=1&page_size=10
```

**Response:**
```json
{
  "users": [...],
  "total": 10,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### ✅ Tạo User
```http
POST /api/users/
Content-Type: application/json

{
  "name": "Nguyễn Văn A",
  "email": "a@example.com"
}
```

### ✅ Lấy User theo ID
```http
GET /api/users/{user_id}
```

### ✅ Update User
```http
PUT /api/users/{user_id}
Content-Type: application/json

{
  "name": "Tên Mới",
  "email": "email@moi.com"
}
```

### ✅ Xóa User
```http
DELETE /api/users/{user_id}
```

---

## 🧪 Test Nhanh với cURL

### 1. Tạo User
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

### 2. Lấy Danh Sách Users
```bash
curl "http://localhost:8000/api/users/?page=1&page_size=10"
```

### 3. Lấy User theo ID
```bash
curl "http://localhost:8000/api/users/YOUR_USER_ID"
```

---

## 📊 Expected Status Codes

| Code | Meaning | Endpoint |
|------|---------|----------|
| 200 | OK | GET, PUT, DELETE |
| 201 | Created | POST (tạo user) |
| 400 | Bad Request | Email trùng, validation error |
| 404 | Not Found | User không tồn tại |
| 422 | Validation Error | Email không hợp lệ |

---

## 🎨 Postman Collection Highlights

### 📦 11 Requests sẵn sàng:
1. ✅ Health Check
2. ✅ Tạo User Mới (auto-save ID)
3. ✅ Lấy Danh Sách Users (pagination)
4. ✅ Lấy User theo ID
5. ✅ Lấy User theo Email
6. ✅ Update User (PUT)
7. ✅ Update User (PATCH)
8. ✅ Xóa User
9. ⚠️ Test - Email Trùng (error case)
10. ⚠️ Test - User Không Tồn Tại (error case)
11. ⚠️ Test - Email Không Hợp Lệ (error case)

### 🎯 Auto Variables:
- `{{base_url}}` - http://localhost:8000
- `{{user_id}}` - Auto-set sau khi tạo user
- `{{user_email}}` - Auto-set sau khi tạo user

---

## 🔥 Quick Demo Flow

```bash
# 1. Start server
python -m BE.main

# 2. Terminal mới - Chạy Python test
python test_with_requests.py

# 3. Hoặc dùng Postman
# Import: User_API.postman_collection.json
# Click "Run Collection"
```

---

## 📚 Chi tiết hơn

- **Postman Guide:** `POSTMAN_GUIDE.md`
- **API Docs:** `BE/README.md`
- **Architecture:** `BE/ARCHITECTURE.md`
- **Quick Start:** `QUICK_START_USER_API.md`

---

## 🐛 Troubleshooting

### ❌ Connection Error
```
Error: connect ECONNREFUSED
```
**Fix:** `python -m BE.main`

### ❌ MongoDB Error
```
Error: SSL handshake failed
```
**Fix:** `python test_connection.py`

---

## 🎉 All Set!

Chọn cách test bạn thích:
- 📮 Postman → Professional
- 🐍 Python Script → Automated
- 📖 Swagger UI → Quick & Easy
- 💻 cURL → Command Line

Happy Testing! 🚀

