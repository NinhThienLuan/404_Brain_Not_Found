# 💬 Chat API Documentation

## Tổng quan

API Chat cung cấp các endpoint để quản lý phòng chat và tin nhắn trong hệ thống AI Code Generation & Review.

**Base URL**: `/api/chat`

---

## 📋 Mục lục

1. [ChatRoom APIs](#chatroom-apis)
   - [Tạo phòng chat mới](#1-tạo-phòng-chat-mới)
   - [Lấy danh sách phòng chat của user](#2-lấy-danh-sách-phòng-chat-của-user)
   - [Lấy chi tiết phòng chat](#3-lấy-chi-tiết-phòng-chat)
   - [Cập nhật tiêu đề phòng chat](#4-cập-nhật-tiêu-đề-phòng-chat)
   - [Xóa phòng chat](#5-xóa-phòng-chat)

2. [Message APIs](#message-apis)
   - [Gửi tin nhắn mới](#1-gửi-tin-nhắn-mới)
   - [Lấy tin nhắn trong phòng chat](#2-lấy-tin-nhắn-trong-phòng-chat)
   - [Lấy chi tiết tin nhắn](#3-lấy-chi-tiết-tin-nhắn)

3. [Luồng hoạt động](#luồng-hoạt-động)

---

## ChatRoom APIs

### 1. Tạo phòng chat mới

**Endpoint**: `POST /api/chat/rooms`

**Mô tả**: Tạo một phòng chat mới cho user

**Request Body**:
```json
{
  "user_id": "507f1f77bcf86cd799439011",
  "title": "Code Review Session" // Optional
}
```

**Response** (201 Created):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "title": "Code Review Session",
  "created_at": "2025-11-02T10:30:00Z",
  "updated_at": "2025-11-02T10:30:00Z",
  "is_active": true
}
```

**Ví dụ cURL**:
```bash
curl -X POST "http://localhost:8000/api/chat/rooms" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "507f1f77bcf86cd799439011",
    "title": "Code Review Session"
  }'
```

---

### 2. Lấy danh sách phòng chat của user

**Endpoint**: `GET /api/chat/rooms/user/{user_id}`

**Mô tả**: Lấy tất cả phòng chat của một user

**Query Parameters**:
- `limit` (optional): Số lượng phòng tối đa (default: 50, max: 100)

**Response** (200 OK):
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "user_id": "507f1f77bcf86cd799439011",
    "title": "Code Review Session",
    "created_at": "2025-11-02T10:30:00Z",
    "updated_at": "2025-11-02T10:30:00Z",
    "is_active": true
  },
  {
    "id": "507f1f77bcf86cd799439013",
    "user_id": "507f1f77bcf86cd799439011",
    "title": "Bug Fix Discussion",
    "created_at": "2025-11-02T09:15:00Z",
    "updated_at": "2025-11-02T09:15:00Z",
    "is_active": true
  }
]
```

**Ví dụ cURL**:
```bash
curl -X GET "http://localhost:8000/api/chat/rooms/user/507f1f77bcf86cd799439011?limit=50"
```

---

### 3. Lấy chi tiết phòng chat

**Endpoint**: `GET /api/chat/rooms/{room_id}`

**Mô tả**: Lấy thông tin chi tiết của một phòng chat

**Response** (200 OK):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "title": "Code Review Session",
  "created_at": "2025-11-02T10:30:00Z",
  "updated_at": "2025-11-02T10:30:00Z",
  "is_active": true
}
```

**Ví dụ cURL**:
```bash
curl -X GET "http://localhost:8000/api/chat/rooms/507f1f77bcf86cd799439012"
```

---

### 4. Cập nhật tiêu đề phòng chat

**Endpoint**: `PUT /api/chat/rooms/{room_id}`

**Mô tả**: Cập nhật tiêu đề của phòng chat

**Request Body**:
```json
{
  "title": "Updated Title"
}
```

**Response** (200 OK):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "title": "Updated Title",
  "created_at": "2025-11-02T10:30:00Z",
  "updated_at": "2025-11-02T11:00:00Z",
  "is_active": true
}
```

**Ví dụ cURL**:
```bash
curl -X PUT "http://localhost:8000/api/chat/rooms/507f1f77bcf86cd799439012" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

---

### 5. Xóa phòng chat

**Endpoint**: `DELETE /api/chat/rooms/{room_id}`

**Mô tả**: Xóa phòng chat (soft delete - đánh dấu is_active = false)

**Response** (200 OK):
```json
{
  "message": "Chat room deleted successfully",
  "room_id": "507f1f77bcf86cd799439012"
}
```

**Ví dụ cURL**:
```bash
curl -X DELETE "http://localhost:8000/api/chat/rooms/507f1f77bcf86cd799439012"
```

---

## Message APIs

### 1. Gửi tin nhắn mới

**Endpoint**: `POST /api/chat/messages`

**Mô tả**: Gửi tin nhắn mới vào phòng chat

**Request Body**:
```json
{
  "chat_room_id": "507f1f77bcf86cd799439012",
  "content": "Can you review this Python code?",
  "sender_type": "user", // "user" hoặc "ai"
  "metadata": { // Optional
    "language": "python",
    "code_snippet": "def hello(): pass"
  }
}
```

**Response** (201 Created):
```json
{
  "id": "507f1f77bcf86cd799439020",
  "chat_room_id": "507f1f77bcf86cd799439012",
  "content": "Can you review this Python code?",
  "sender_type": "user",
  "created_at": "2025-11-02T10:35:00Z",
  "metadata": {
    "language": "python",
    "code_snippet": "def hello(): pass"
  }
}
```

**Ví dụ cURL**:
```bash
curl -X POST "http://localhost:8000/api/chat/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_room_id": "507f1f77bcf86cd799439012",
    "content": "Can you review this Python code?",
    "sender_type": "user"
  }'
```

---

### 2. Lấy tin nhắn trong phòng chat

**Endpoint**: `GET /api/chat/messages/room/{chat_room_id}`

**Mô tả**: Lấy danh sách tin nhắn trong một phòng chat

**Query Parameters**:
- `limit` (optional): Số lượng tin nhắn tối đa (default: 100, max: 500)
- `skip` (optional): Số lượng tin nhắn bỏ qua (default: 0) - dùng cho pagination

**Response** (200 OK):
```json
{
  "messages": [
    {
      "id": "507f1f77bcf86cd799439020",
      "chat_room_id": "507f1f77bcf86cd799439012",
      "content": "Can you review this Python code?",
      "sender_type": "user",
      "created_at": "2025-11-02T10:35:00Z",
      "metadata": {}
    },
    {
      "id": "507f1f77bcf86cd799439021",
      "chat_room_id": "507f1f77bcf86cd799439012",
      "content": "Sure! The code looks good but...",
      "sender_type": "ai",
      "created_at": "2025-11-02T10:35:05Z",
      "metadata": {}
    }
  ],
  "total": 2,
  "chat_room_id": "507f1f77bcf86cd799439012"
}
```

**Ví dụ cURL**:
```bash
curl -X GET "http://localhost:8000/api/chat/messages/room/507f1f77bcf86cd799439012?limit=100&skip=0"
```

---

### 3. Lấy chi tiết tin nhắn

**Endpoint**: `GET /api/chat/messages/{message_id}`

**Mô tả**: Lấy thông tin chi tiết của một tin nhắn

**Response** (200 OK):
```json
{
  "id": "507f1f77bcf86cd799439020",
  "chat_room_id": "507f1f77bcf86cd799439012",
  "content": "Can you review this Python code?",
  "sender_type": "user",
  "created_at": "2025-11-02T10:35:00Z",
  "metadata": {}
}
```

**Ví dụ cURL**:
```bash
curl -X GET "http://localhost:8000/api/chat/messages/507f1f77bcf86cd799439020"
```

---

## Luồng hoạt động

### 🔄 Luồng chính khi user tương tác với chatbox

```
1. User mở ứng dụng
   ↓
2. GET /api/chat/rooms/user/{user_id}
   → Lấy danh sách phòng chat của user
   ↓
3. User tạo phòng chat mới (nếu cần)
   POST /api/chat/rooms
   → Tạo phòng chat mới
   ↓
4. User chọn một phòng chat
   GET /api/chat/messages/room/{chat_room_id}
   → Lấy lịch sử tin nhắn
   ↓
5. User gửi tin nhắn
   POST /api/chat/messages
   {
     "chat_room_id": "...",
     "content": "Can you help me with...",
     "sender_type": "user"
   }
   ↓
6. AI xử lý và trả lời (được xử lý bởi team khác)
   POST /api/chat/messages
   {
     "chat_room_id": "...",
     "content": "Sure! Here's the solution...",
     "sender_type": "ai",
     "metadata": {
       "code": "...",
       "language": "python"
     }
   }
```

### 🔄 Luồng quản lý phòng chat từ thanh bên

```
1. User xem danh sách phòng chat
   GET /api/chat/rooms/user/{user_id}
   ↓
2. User tạo phòng chat mới
   POST /api/chat/rooms
   ↓
3. User đổi tên phòng chat
   PUT /api/chat/rooms/{room_id}
   {"title": "New Title"}
   ↓
4. User xóa phòng chat
   DELETE /api/chat/rooms/{room_id}
```

---

## 🛠️ Integration với các module khác

### Với AI Service (code generation/review)

Khi AI service xử lý xong request của user, nó sẽ gọi:

```python
# Ví dụ code trong AI service
POST /api/chat/messages
{
  "chat_room_id": "{room_id_from_request}",
  "content": "{ai_response}",
  "sender_type": "ai",
  "metadata": {
    "type": "code_generation", // hoặc "code_review"
    "language": "python",
    "code": "{generated_code}",
    "review_score": 85 // nếu là review
  }
}
```

### Với Frontend

Frontend cần:
1. **Polling hoặc WebSocket** để nhận tin nhắn mới real-time
2. **Local state management** để quản lý chat rooms và messages
3. **Optimistic updates** để UX mượt mà hơn

---

## 📝 Notes

1. **Soft Delete**: Phòng chat không bị xóa vĩnh viễn, chỉ đánh dấu `is_active = false`
2. **Pagination**: Dùng `skip` và `limit` để phân trang tin nhắn
3. **Metadata**: Field linh hoạt để lưu thêm thông tin (code, language, score, etc.)
4. **sender_type**: Chỉ có 2 giá trị: `"user"` hoặc `"ai"`

---

## 🚀 Quick Test

Chạy server:
```bash
cd BE
python -m uvicorn main:app --reload
```

Truy cập docs:
```
http://localhost:8000/docs
```

Test các endpoints ngay trên Swagger UI! 🎉
