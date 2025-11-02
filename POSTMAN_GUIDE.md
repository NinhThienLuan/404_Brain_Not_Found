# 📮 Hướng Dẫn Test API Với Postman

## 🚀 Bước 1: Chuẩn bị

### 1.1. Chạy Server

```bash
python -m BE.main
```

Server sẽ chạy tại: **http://localhost:8000**

### 1.2. Cài đặt Postman

- Download tại: https://www.postman.com/downloads/
- Hoặc dùng Postman Web: https://web.postman.com/

---

## 📥 Bước 2: Import Collection

### Cách 1: Import File JSON

1. Mở Postman
2. Click **Import** ở góc trên bên trái
3. Chọn file **`User_API.postman_collection.json`**
4. Click **Import**

### Cách 2: Import từ URL (nếu có)

1. Click **Import** > **Link**
2. Paste URL của collection
3. Click **Continue** > **Import**

---

## ⚙️ Bước 3: Cấu hình Variables

Collection đã có sẵn 3 variables:

| Variable | Giá trị mặc định | Mô tả |
|----------|------------------|-------|
| `base_url` | `http://localhost:8000` | URL của server |
| `user_id` | (auto-set) | ID của user vừa tạo |
| `user_email` | (auto-set) | Email của user vừa tạo |

**Thay đổi base_url** (nếu cần):
1. Click vào collection
2. Tab **Variables**
3. Thay đổi giá trị `base_url`
4. Click **Save**

---

## 🧪 Bước 4: Test API Endpoints

### ✅ **1. Health Check**

**Request:**
```
GET http://localhost:8000/
```

**Expected Response:** `200 OK`
```json
{
  "status": "OK",
  "message": "Hackathon API đang chạy!",
  "docs": "/docs"
}
```

---

### ✅ **2. Tạo User Mới**

**Request:**
```
POST http://localhost:8000/api/users/
Content-Type: application/json

{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com"
}
```

**Expected Response:** `201 Created`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

> 💡 **Tip:** Request này tự động lưu `user_id` và `user_email` vào variables!

---

### ✅ **3. Lấy Danh Sách Users**

**Request:**
```
GET http://localhost:8000/api/users/?page=1&page_size=10
```

**Parameters:**
- `page`: Số trang (default: 1)
- `page_size`: Số users mỗi trang (default: 10, max: 100)

**Expected Response:** `200 OK`
```json
{
  "users": [
    {
      "_id": "6906ae5b2484813d2b42c6db",
      "name": "Nguyễn Văn A",
      "email": "nguyenvana@example.com",
      "created_at": "2025-11-02T01:05:31.153Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

**Thử nghiệm pagination:**
- `?page=1&page_size=5` - Lấy 5 users đầu
- `?page=2&page_size=5` - Lấy 5 users tiếp theo

---

### ✅ **4. Lấy User Theo ID**

**Request:**
```
GET http://localhost:8000/api/users/{{user_id}}
```

> Sử dụng variable `{{user_id}}` được set tự động từ request tạo user

**Expected Response:** `200 OK`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

---

### ✅ **5. Lấy User Theo Email**

**Request:**
```
GET http://localhost:8000/api/users/email/{{user_email}}
```

**Expected Response:** `200 OK`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

---

### ✅ **6. Update User (PUT)**

**Request:**
```
PUT http://localhost:8000/api/users/{{user_id}}
Content-Type: application/json

{
  "name": "Nguyễn Văn A Updated",
  "email": "updated@example.com"
}
```

**Expected Response:** `200 OK`
```json
{
  "_id": "6906ae5b2484813d2b42c6db",
  "name": "Nguyễn Văn A Updated",
  "email": "updated@example.com",
  "created_at": "2025-11-02T01:05:31.153Z"
}
```

---

### ✅ **7. Update User (PATCH)**

**Request:**
```
PATCH http://localhost:8000/api/users/{{user_id}}
Content-Type: application/json

{
  "name": "Tên Mới"
}
```

> Chỉ update name, email giữ nguyên

**Expected Response:** `200 OK`

---

### ✅ **8. Xóa User**

**Request:**
```
DELETE http://localhost:8000/api/users/{{user_id}}
```

**Expected Response:** `200 OK`
```json
{
  "message": "Đã xóa user với ID '...' thành công"
}
```

---

## 🧪 Test Error Cases

### ❌ **Test 1: Email Trùng**

**Request:**
```
POST http://localhost:8000/api/users/
Content-Type: application/json

{
  "name": "User Khác",
  "email": "nguyenvana@example.com"
}
```

**Expected Response:** `400 Bad Request`
```json
{
  "detail": "Email 'nguyenvana@example.com' đã tồn tại trong hệ thống"
}
```

---

### ❌ **Test 2: User Không Tồn Tại**

**Request:**
```
GET http://localhost:8000/api/users/invalid_id_12345
```

**Expected Response:** `404 Not Found`
```json
{
  "detail": "Không tìm thấy user với ID 'invalid_id_12345'"
}
```

---

### ❌ **Test 3: Email Không Hợp Lệ**

**Request:**
```
POST http://localhost:8000/api/users/
Content-Type: application/json

{
  "name": "Test User",
  "email": "not-an-email"
}
```

**Expected Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 🎯 Test Flow Hoàn Chỉnh

### Scenario 1: CRUD Flow

1. **Health Check** ✅
2. **Tạo User** ✅ → Lưu `user_id`
3. **Lấy User theo ID** ✅ → Verify user vừa tạo
4. **Lấy Danh Sách Users** ✅ → Verify user có trong list
5. **Update User** ✅ → Thay đổi thông tin
6. **Lấy User theo ID** ✅ → Verify đã update
7. **Xóa User** ✅ → Remove user
8. **Lấy User theo ID** ❌ → Verify đã bị xóa (404)

### Scenario 2: Pagination Test

1. **Tạo 15 users** (chạy request tạo user 15 lần với email khác nhau)
2. **Lấy page 1** (`?page=1&page_size=10`) → 10 users
3. **Lấy page 2** (`?page=2&page_size=10`) → 5 users
4. **Verify total** → total = 15, total_pages = 2

---

## 🔧 Tips & Tricks

### 1. **Chạy Toàn Bộ Collection**

- Click vào collection name
- Click **Run** (hoặc ⌘+R / Ctrl+R)
- Click **Run User CRUD API**
- Xem kết quả từng request

### 2. **Environment Variables**

Tạo environment riêng cho dev/staging/production:

1. Click **Environments** (icon bánh răng)
2. Click **+** để tạo environment mới
3. Thêm variable `base_url` với giá trị khác nhau
4. Switch environment khi test

**Example:**
```
Development: http://localhost:8000
Staging: https://staging.yourapp.com
Production: https://api.yourapp.com
```

### 3. **Auto-save Variables**

Request **"1. Tạo User Mới"** có script tự động lưu `user_id`:

```javascript
if (pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("user_id", jsonData._id);
    pm.environment.set("user_email", jsonData.email);
}
```

### 4. **Tests/Assertions**

Thêm tests vào tab **Tests** của mỗi request:

```javascript
// Test status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response body
pm.test("User has name", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.name).to.exist;
});

// Test response time
pm.test("Response time < 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

---

## 📊 Response Status Codes

| Code | Meaning | Khi nào xảy ra |
|------|---------|----------------|
| 200 | OK | Request thành công (GET, PUT, DELETE) |
| 201 | Created | Tạo user thành công (POST) |
| 400 | Bad Request | Validation error (email trùng, data không hợp lệ) |
| 404 | Not Found | User không tồn tại |
| 422 | Unprocessable Entity | Pydantic validation error |
| 500 | Internal Server Error | Lỗi server (database error, etc.) |

---

## 🎨 Swagger UI Alternative

Nếu không muốn dùng Postman, có thể test trực tiếp qua Swagger UI:

1. Mở: http://localhost:8000/docs
2. Click vào endpoint muốn test
3. Click **"Try it out"**
4. Nhập data
5. Click **"Execute"**

**Lợi ích Swagger:**
- ✅ Built-in, không cần install gì
- ✅ Auto-generated từ code
- ✅ Interactive testing

**Lợi ích Postman:**
- ✅ Save requests
- ✅ Collections & folders
- ✅ Environment variables
- ✅ Automated testing
- ✅ Team collaboration

---

## 📸 Screenshots Guide

### Import Collection
1. Click **Import**
2. Drag & drop file JSON
3. Click **Import**

### View Variables
1. Click collection name
2. Tab **Variables**
3. Xem `base_url`, `user_id`, `user_email`

### Run Request
1. Click vào request
2. Click **Send**
3. Xem response ở dưới

---

## 🐛 Troubleshooting

### Lỗi: Connection refused
```
Error: connect ECONNREFUSED 127.0.0.1:8000
```
**Giải pháp:** Server chưa chạy → `python -m BE.main`

### Lỗi: 404 Not Found
```
{
  "detail": "Not Found"
}
```
**Giải pháp:** Sai URL, kiểm tra lại endpoint

### Lỗi: 500 Internal Server Error
```
{
  "detail": "Lỗi khi tạo user: ..."
}
```
**Giải pháp:** 
- Kiểm tra MongoDB connection
- Xem server logs
- Chạy `python test_connection.py`

---

## 🎉 Happy Testing!

Có vấn đề gì không rõ? Check:
- **API Docs:** http://localhost:8000/docs
- **README:** `BE/README.md`
- **Architecture:** `BE/ARCHITECTURE.md`

