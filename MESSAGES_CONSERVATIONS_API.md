# 💬 Messages & Conservations API Guide

## 📋 Overview:

Đã tạo **CRUD hoàn chỉnh** cho **Messages** và **Conservations** với relationship 1-to-many.

### **Relationship:**
```
Conservation (1) ←── (many) Messages
```

- Một conservation có nhiều messages
- Message có `conversationId` link tới conservation
- Tự động update `messageCount` khi tạo/xóa message

---

## 📊 Entity Structures:

### **Conservation Entity:**
```python
- id: str
- title: str                    # Tiêu đề
- goal: str                     # Mục tiêu
- message_count: int            # Số lượng messages
- facts: List[str]              # Array of facts
- created_at: datetime
- updated_at: datetime
```

**MongoDB Structure:**
```json
{
  "_id": "6905a4bada4db5565a169084",
  "title": "test",
  "goal": "trang index.html",
  "messageCount": 19,
  "facts": ["fact1", "fact2", ...],
  "createdAt": "2025-11-01T06:12:10.341Z",
  "updatedAt": "2025-11-01T06:18:19.060Z"
}
```

---

### **Message Entity:**
```python
- id: str
- conversation_id: str          # Link to conservation
- sender: str                   # "system" hoặc "user"
- text: str                     # Nội dung
- type: str                     # "text"
- created_at: datetime
- updated_at: datetime
- v: int                        # __v field
```

**MongoDB Structure:**
```json
{
  "_id": "6905a37f9d893e353a0c5fc2",
  "conversationId": "6905a37e9d893e353a0c5fc0",
  "sender": "system",
  "text": "Chào bạn, bạn cần tôi hỗ trợ tạo Figma cho trang nào?",
  "type": "text",
  "createdAt": "2025-11-01T06:06:55.090Z",
  "updatedAt": "2025-11-01T06:06:55.090Z",
  "__v": 0
}
```

---

## 🎯 API Endpoints:

### **Conservations** (`/api/conservations`) - 7 endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/conservations/` | Tạo conservation mới |
| GET | `/api/conservations/{id}` | Lấy conservation theo ID |
| GET | `/api/conservations/{id}/with-messages` | Lấy conservation + messages |
| GET | `/api/conservations/` | List conservations |
| GET | `/api/conservations/?title=xxx` | Search by title |
| GET | `/api/conservations/?recent=true` | Lấy recent conservations |
| PUT | `/api/conservations/{id}` | Update conservation |
| POST | `/api/conservations/{id}/facts` | Thêm fact |
| DELETE | `/api/conservations/{id}` | Xóa conservation |

---

### **Messages** (`/api/messages`) - 6 endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/messages/` | Tạo message mới |
| GET | `/api/messages/{id}` | Lấy message theo ID |
| GET | `/api/messages/` | List tất cả messages |
| GET | `/api/messages/conversation/{id}` | Lấy messages của conversation |
| PUT | `/api/messages/{id}` | Update message text |
| DELETE | `/api/messages/{id}` | Xóa message |

---

## 🚀 Usage Examples:

### **1. Tạo Conservation:**

**Request:**
```bash
curl -X POST "http://localhost:8000/api/conservations/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design Landing Page",
    "goal": "Tạo Figma cho trang chủ",
    "facts": ["Use modern design", "Mobile first"]
  }'
```

**Response:** `201 Created`
```json
{
  "_id": "6905a4bada4db5565a169084",
  "title": "Design Landing Page",
  "goal": "Tạo Figma cho trang chủ",
  "messageCount": 0,
  "facts": ["Use modern design", "Mobile first"],
  "createdAt": "2025-11-01T06:12:10.341Z",
  "updatedAt": "2025-11-01T06:12:10.341Z"
}
```

---

### **2. Tạo Message trong Conservation:**

**Request:**
```bash
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "conversationId": "6905a4bada4db5565a169084",
    "sender": "user",
    "text": "Bạn có thể làm được gì?",
    "type": "text"
  }'
```

**Response:** `201 Created`
```json
{
  "_id": "6905a38b9d893e353a0c5fc8",
  "conversationId": "6905a4bada4db5565a169084",
  "sender": "user",
  "text": "Bạn có thể làm được gì?",
  "type": "text",
  "createdAt": "2025-11-01T06:07:07.913Z",
  "updatedAt": "2025-11-01T06:07:07.913Z",
  "__v": 0
}
```

> ✨ **Auto feature:** Conservation `messageCount` tự động tăng lên 1!

---

### **3. Lấy Conservation với Messages:**

**Request:**
```bash
curl "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/with-messages"
```

**Response:** `200 OK`
```json
{
  "conservation": {
    "_id": "6905a4bada4db5565a169084",
    "title": "Design Landing Page",
    "goal": "Tạo Figma cho trang chủ",
    "messageCount": 2,
    "facts": ["Use modern design", "Mobile first"]
  },
  "messages": [
    {
      "_id": "6905a37f9d893e353a0c5fc2",
      "conversationId": "6905a4bada4db5565a169084",
      "sender": "system",
      "text": "Chào bạn, bạn cần tôi hỗ trợ tạo Figma cho trang nào?"
    },
    {
      "_id": "6905a38b9d893e353a0c5fc8",
      "conversationId": "6905a4bada4db5565a169084",
      "sender": "user",
      "text": "Bạn có thể làm được gì?"
    }
  ],
  "totalMessages": 2
}
```

---

### **4. Lấy Messages của Conservation:**

**Request:**
```bash
curl "http://localhost:8000/api/messages/conversation/6905a4bada4db5565a169084?page=1&page_size=50"
```

**Response:** `200 OK`
```json
{
  "items": [
    {...message 1...},
    {...message 2...}
  ],
  "total": 2,
  "page": 1,
  "page_size": 50,
  "total_pages": 1,
  "conversationId": "6905a4bada4db5565a169084"
}
```

---

### **5. Thêm Fact vào Conservation:**

**Request:**
```bash
curl -X POST "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/facts" \
  -H "Content-Type: application/json" \
  -d '{
    "fact": "User prefers blue color scheme"
  }'
```

**Response:** `200 OK`
```json
{
  "_id": "6905a4bada4db5565a169084",
  "title": "Design Landing Page",
  "goal": "Tạo Figma cho trang chủ",
  "messageCount": 2,
  "facts": [
    "Use modern design",
    "Mobile first",
    "User prefers blue color scheme"
  ]
}
```

---

### **6. Search Conservations:**

**Request:**
```bash
# Search by title
curl "http://localhost:8000/api/conservations/?title=Design"

# Get recent conservations
curl "http://localhost:8000/api/conservations/?recent=true"
```

---

### **7. Update Message:**

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/messages/6905a38b9d893e353a0c5fc8" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bạn có thể làm gì cho tôi?"
  }'
```

---

### **8. Xóa Conservation (+ Messages):**

**Request:**
```bash
# Xóa conservation và tất cả messages
curl -X DELETE "http://localhost:8000/api/conservations/6905a4bada4db5565a169084?delete_messages=true"

# Xóa chỉ conservation (giữ messages)
curl -X DELETE "http://localhost:8000/api/conservations/6905a4bada4db5565a169084?delete_messages=false"
```

---

## 🔗 Relationships & Business Logic:

### **Auto Message Count:**

Khi tạo message → **Conservation.messageCount tự động tăng**

```python
# Service layer
def create_message(...):
    message = self.repo.create(message)
    self.conservation_repo.increment_message_count(conversation_id)
    return message
```

Khi xóa message → **Conservation.messageCount tự động giảm**

```python
def delete_message(..., update_count=True):
    success = self.repo.delete(message_id)
    if update_count:
        self.conservation_repo.decrement_message_count(...)
    return success
```

---

### **Cascade Delete:**

Xóa conservation có thể xóa luôn messages:

```python
def delete_conservation(id, delete_messages=True):
    if delete_messages:
        self.message_repo.delete_by_conversation(id)
    self.repo.delete(id)
```

---

## 🏗️ Architecture Flow:

### **Tạo Message Flow:**

```
1. Client Request
   POST /api/messages/
   {
     "conversationId": "xxx",
     "sender": "user",
     "text": "Hello"
   }

2. Controller (message_controller.py)
   ├─ Validate request (Pydantic)
   └─ Call service.create_message()

3. Service (message_service.py)
   ├─ Validate sender ("system" hoặc "user")
   ├─ Check conservation exists
   ├─ Create Message entity
   ├─ Call repo.create()
   └─ Call conservation_repo.increment_message_count() ← Auto!

4. Repository (message_repo.py)
   ├─ Convert entity to dict
   ├─ Insert into MongoDB
   └─ Return Message entity

5. ConservationRepository
   └─ Update messageCount +1

6. Response
   {
     "_id": "...",
     "conversationId": "...",
     ...
   }
```

---

## 🎨 Special Features:

### **1. Auto Message Count**
✅ Tạo message → count +1  
✅ Xóa message → count -1  
✅ Không cần update thủ công  

### **2. Get Conservation with Messages**
✅ Một endpoint lấy cả conservation và messages  
✅ Tiện cho chat UI  

### **3. Search by Title**
✅ Partial match, case-insensitive  
✅ Dùng regex  

### **4. Recent Conservations**
✅ Sorted by createdAt DESC  
✅ Lấy conversations mới nhất  

### **5. Add Facts**
✅ Thêm fact vào array  
✅ Auto update updatedAt  

### **6. Cascade Delete**
✅ Xóa conservation + messages cùng lúc  
✅ Hoặc giữ messages nếu muốn  

---

## 📊 Query Parameters:

### **Conservations:**
- `page` - Số trang (default: 1)
- `page_size` - Items per page (default: 10, max: 100)
- `title` - Search by title
- `recent` - Get recent conservations (true/false)

### **Messages:**
- `page` - Số trang (default: 1)
- `page_size` - Messages per page (default: 50, max: 200)

---

## 🧪 Testing Examples:

### **Scenario 1: Chat Flow**

```bash
# 1. Tạo conservation
CONSERVATION_ID=$(curl -X POST "http://localhost:8000/api/conservations/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat","goal":"Testing"}' \
  | jq -r '._id')

# 2. System gửi message
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d "{\"conversationId\":\"$CONSERVATION_ID\",\"sender\":\"system\",\"text\":\"Hello!\"}"

# 3. User reply
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d "{\"conversationId\":\"$CONSERVATION_ID\",\"sender\":\"user\",\"text\":\"Hi!\"}"

# 4. Lấy conversation với messages
curl "http://localhost:8000/api/conservations/$CONSERVATION_ID/with-messages"
```

---

### **Scenario 2: Search & Filter**

```bash
# Search conservations
curl "http://localhost:8000/api/conservations/?title=design"

# Get recent conservations
curl "http://localhost:8000/api/conservations/?recent=true&page_size=5"

# Get messages of a conversation
curl "http://localhost:8000/api/messages/conversation/6905a4bada4db5565a169084"
```

---

## 🎯 Use Cases:

### **Chat Application:**
```javascript
// Frontend example
async function sendMessage(conversationId, text) {
  const response = await fetch('/api/messages/', {
    method: 'POST',
    body: JSON.stringify({
      conversationId,
      sender: 'user',
      text
    })
  });
  return response.json();
}

async function loadChat(conversationId) {
  const response = await fetch(`/api/conservations/${conversationId}/with-messages`);
  const data = await response.json();
  
  // data.conservation - Conservation info
  // data.messages - All messages
  // data.totalMessages - Count
  
  return data;
}
```

---

## 📝 Validation Rules:

### **Conservation:**
- ✅ `title` - Required, không empty
- ✅ `goal` - Required, không empty
- ✅ `facts` - Optional array

### **Message:**
- ✅ `conversationId` - Required, phải tồn tại
- ✅ `sender` - Required, phải là "system" hoặc "user"
- ✅ `text` - Required, không empty
- ✅ `type` - Default "text"

---

## 🔄 Auto Features:

### **1. Message Count Auto Update:**
```
Create message → messageCount +1
Delete message → messageCount -1
```

### **2. Timestamps Auto Update:**
```
Create → createdAt, updatedAt = now()
Update → updatedAt = now()
Add fact → updatedAt = now()
```

### **3. Cascade Delete:**
```
Delete conservation (delete_messages=true)
  ↓
Delete all messages của conservation
  ↓
Delete conservation
```

---

## 🎨 Advanced Queries:

### **Get Messages by Sender:**

Repository có method `find_by_sender()`:
```python
# Trong service có thể thêm:
def get_system_messages(page, page_size):
    return self.repo.find_by_sender("system", skip, limit)
```

### **Count Messages by Conservation:**

```python
count = message_repo.count_by_conversation(conservation_id)
```

---

## 📊 Response Formats:

### **Single Conservation:**
```json
{
  "_id": "...",
  "title": "...",
  "goal": "...",
  "messageCount": 19,
  "facts": [...],
  "createdAt": "...",
  "updatedAt": "..."
}
```

### **Conservation with Messages:**
```json
{
  "conservation": {...},
  "messages": [
    {
      "_id": "...",
      "conversationId": "...",
      "sender": "system",
      "text": "...",
      ...
    }
  ],
  "totalMessages": 2
}
```

### **Paginated List:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10
}
```

---

## 🔍 Current Data trong MongoDB:

Từ images:

### **Conservations:**
- 1 conservation với:
  - title: "test"
  - goal: "trang index.html"
  - messageCount: 19
  - facts: 12 items

### **Messages:**
- Nhiều messages với:
  - conversationId link tới conservation
  - sender: "system" hoặc "user"
  - text: Vietnamese content

---

## 🧪 Test với Swagger UI:

Mở: **http://localhost:8000/docs**

Bạn sẽ thấy 2 groups mới:
1. **Conservations** - 7 endpoints
2. **Messages** - 6 endpoints

**Try it out:**
1. Click endpoint
2. Click "Try it out"
3. Fill data
4. Click "Execute"
5. See response!

---

## ✨ Key Features:

✅ **1-to-many relationship** - Conservation → Messages  
✅ **Auto message count** - Tự động update  
✅ **Cascade delete** - Xóa conservation + messages  
✅ **Search support** - Search by title  
✅ **Recent sorting** - Get newest conservations  
✅ **Facts management** - Add facts dynamically  
✅ **Pagination** - Hiệu quả với nhiều data  
✅ **Validation** - Business rules enforced  

---

## 🎯 Common Workflows:

### **Chat Workflow:**
1. Tạo conservation
2. System gửi welcome message
3. User reply
4. System response
5. Repeat...
6. Get conservation with all messages để display

### **Conservation Management:**
1. List all conservations
2. Search by title
3. Click vào conservation
4. Load conservation + messages
5. Send new message
6. Update conservation info nếu cần

---

## 📚 Related Endpoints:

### **Conservation + Messages:**
```
GET /api/conservations/{id}/with-messages
```
→ Lấy everything cùng lúc!

### **Conservation Messages Only:**
```
GET /api/messages/conversation/{id}
```
→ Chỉ lấy messages (có pagination)

---

## 🔥 Production Ready!

✅ Type-safe entities  
✅ Business logic validated  
✅ Auto message counting  
✅ Cascade delete support  
✅ Search functionality  
✅ Pagination optimized  
✅ Error handling complete  

**Test ngay:** http://localhost:8000/docs 🚀

---

Happy Coding! 💬✨

