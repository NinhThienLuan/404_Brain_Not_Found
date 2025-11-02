# 🚀 Hướng Dẫn Sử Dụng API - 404 Brain Not Found

## ⚡ Chạy Server Ngay (1 dòng):

```bash
python -m BE.main
```

Mở: **http://localhost:8000/docs** ✅

---

## 📊 Đã có 8 APIs sẵn sàng:

| API | Endpoint | Tính năng | Data có sẵn |
|-----|----------|-----------|-------------|
| 👥 Users | `/api/users` | Quản lý user | 2 users |
| 💬 Conservations | `/api/conservations` | Quản lý hội thoại | 1 conversation |
| 📨 Messages | `/api/messages` | Tin nhắn chat | Nhiều messages |
| 📝 Requests | `/api/requests` | Yêu cầu user | 3 requests |
| 🚀 Code Generations | `/api/code-generations` | Code đã tạo | 1 generation |
| 🔍 Code Reviews | `/api/code-reviews` | Kết quả review | 1 review |
| 📊 Execution Logs | `/api/execution-logs` | Log chạy code | 1 log |
| 🏠 Chat Rooms | `/api/chat-rooms` | Phòng chat | 1 room |

**Total: 8 APIs với 41+ endpoints!**

---

## 🎯 Tính năng đặc biệt:

### **Messages & Conservations** ⭐ MỚI TẠO:

✨ **Auto message count:**
- Tạo message → Conservation tự động +1 message
- Xóa message → Conservation tự động -1 message

✨ **Lấy conservation + messages:**
```bash
GET /api/conservations/{id}/with-messages
```
→ Lấy hội thoại và tất cả tin nhắn cùng lúc!

✨ **Search conservations:**
```bash
GET /api/conservations/?title=test
```

✨ **Thêm facts:**
```bash
POST /api/conservations/{id}/facts
{"fact": "User likes Python"}
```

✨ **Cascade delete:**
```bash
DELETE /api/conservations/{id}?delete_messages=true
```
→ Xóa conversation và tất cả messages!

---

## 🧪 Test Ngay:

### **1. Swagger UI** (Dễ nhất):
```
http://localhost:8000/docs
```

Chọn endpoint → **Try it out** → Nhập data → **Execute**

### **2. Test với cURL:**

```bash
# Lấy conservations
curl "http://localhost:8000/api/conservations/"

# Lấy messages
curl "http://localhost:8000/api/messages/"

# Lấy conservation với messages
curl "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/with-messages"
```

### **3. Xem MongoDB:**

```bash
python inspect_collections.py
```

---

## 📝 Ví dụ Chat Flow:

### **Bước 1: Tạo Conservation**
```bash
curl -X POST "http://localhost:8000/api/conservations/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hỗ trợ code Python",
    "goal": "Giúp user học Python",
    "facts": []
  }'
```

→ Nhận conservation_id

### **Bước 2: System gửi message**
```bash
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "conversationId": "CONSERVATION_ID",
    "sender": "system",
    "text": "Xin chào! Bạn muốn học Python điều gì?"
  }'
```

→ Conservation messageCount = 1

### **Bước 3: User reply**
```bash
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "conversationId": "CONSERVATION_ID",
    "sender": "user",
    "text": "Tôi muốn học FastAPI"
  }'
```

→ Conservation messageCount = 2

### **Bước 4: Lấy toàn bộ chat**
```bash
curl "http://localhost:8000/api/conservations/CONSERVATION_ID/with-messages"
```

→ Nhận conservation + tất cả messages!

---

## 🏗️ Cấu trúc Code:

```
Controller (API endpoints)
    ↓
Service (Business logic)
    ↓
Repository (MongoDB operations)
    ↓
Entity (Domain model)
    ↓
MongoDB
```

---

## 🎨 Auto Features:

### **Message Service:**
- ✅ Tự động validate sender ("system" hoặc "user")
- ✅ Tự động check conservation tồn tại
- ✅ Tự động update conservation message count
- ✅ Tự động update timestamps

### **Conservation Service:**
- ✅ Validation title và goal
- ✅ Search by title (partial match)
- ✅ Get recent conservations
- ✅ Add facts dynamically
- ✅ Cascade delete messages

---

## 📊 MongoDB Collections:

```
✓ users...................... 2 documents
✓ conservations.............. 1 documents
✓ messages................... Many documents
✓ requests................... 3 documents
✓ code_generations........... 1 documents
✓ code_reviews............... 1 documents
✓ execution_logs............. 1 documents
✓ chat_rooms................. 1 documents
```

---

## 🎯 Endpoints Highlights:

### **Conservation Endpoints:**
```
POST   /api/conservations/                    - Tạo mới
GET    /api/conservations/{id}                - Chi tiết
GET    /api/conservations/{id}/with-messages  - Với messages
GET    /api/conservations/?title=xxx          - Search
GET    /api/conservations/?recent=true        - Recent
PUT    /api/conservations/{id}                - Update
POST   /api/conservations/{id}/facts          - Add fact
DELETE /api/conservations/{id}                - Xóa
```

### **Message Endpoints:**
```
POST   /api/messages/                         - Tạo mới
GET    /api/messages/{id}                     - Chi tiết
GET    /api/messages/conversation/{id}        - By conversation
PUT    /api/messages/{id}                     - Update text
DELETE /api/messages/{id}                     - Xóa
```

---

## 🎉 HOÀN TẤT!

Tất cả **8 entities** đã có CRUD API hoàn chỉnh:

✅ Users  
✅ Conservations ⭐ NEW  
✅ Messages ⭐ NEW  
✅ Requests  
✅ Code Generations  
✅ Code Reviews  
✅ Execution Logs  
✅ Chat Rooms  

**Test ngay:** http://localhost:8000/docs 🚀

---

## 📚 Docs Chi Tiết:

- **MESSAGES_CONSERVATIONS_API.md** - Chi tiết Messages & Conservations
- **COMPLETE_API_SUMMARY.md** - Tổng kết tất cả APIs
- **API_QUICK_REFERENCE.md** - Reference nhanh

---

Chúc bạn code vui vẻ! 🎊✨

