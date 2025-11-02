# 💬 Chatbox API Guide - Messages & Conservations

## 🎯 Nested Endpoints cho Chatbox UI

Đã thêm **2 endpoints đặc biệt** để dễ tích hợp với chatbox frontend:

### ✅ **1. Thêm Message vào Conservation**
```
POST /api/conservations/{conservation_id}/messages
```

### ✅ **2. Xóa Message từ Conservation**
```
DELETE /api/conservations/{conservation_id}/messages/{message_id}
```

---

## 🚀 Usage cho Frontend:

### **Khi User gửi message trong Chatbox:**

**Request:**
```javascript
// Frontend code
async function sendMessage(conservationId, messageText) {
  const response = await fetch(`/api/conservations/${conservationId}/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      sender: 'user',
      text: messageText,
      type: 'text'
    })
  });
  
  return response.json();
}

// Usage
const message = await sendMessage('6905a4bada4db5565a169084', 'Xin chào!');
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "user",
    "text": "Xin chào!",
    "type": "text"
  }'
```

**Response:** `201 Created`
```json
{
  "_id": "6905a38b9d893e353a0c5fc8",
  "conversationId": "6905a4bada4db5565a169084",
  "sender": "user",
  "text": "Xin chào!",
  "type": "text",
  "createdAt": "2025-11-01T06:07:07.913Z",
  "updatedAt": "2025-11-01T06:07:07.913Z",
  "__v": 0
}
```

✨ **Auto features:**
- ✅ Conservation `messageCount` tự động +1
- ✅ Conservation `updatedAt` tự động update
- ✅ Message được tạo với timestamps
- ✅ Validation sender ("system" hoặc "user")

---

### **Khi User xóa message:**

**Request:**
```javascript
// Frontend code
async function deleteMessage(conservationId, messageId) {
  const response = await fetch(
    `/api/conservations/${conservationId}/messages/${messageId}`,
    {
      method: 'DELETE'
    }
  );
  
  return response.json();
}

// Usage
await deleteMessage('6905a4bada4db5565a169084', '6905a38b9d893e353a0c5fc8');
```

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/messages/6905a38b9d893e353a0c5fc8"
```

**Response:** `200 OK`
```json
{
  "message": "Message đã được xóa khỏi conservation"
}
```

✨ **Auto features:**
- ✅ Verify message thuộc conservation (security)
- ✅ Conservation `messageCount` tự động -1
- ✅ Conservation `updatedAt` tự động update
- ✅ Error nếu message không thuộc conservation

---

## 📊 So sánh 2 cách:

### **Cách 1: Direct Endpoints** (Cũ)

```javascript
// Tạo message - phải truyền conversationId trong body
POST /api/messages/
{
  "conversationId": "6905a4ba...",  // ← Phải nhập
  "sender": "user",
  "text": "Hello"
}
```

### **Cách 2: Nested Endpoints** (Mới - Cho Chatbox) ⭐

```javascript
// Tạo message - conversationId trong URL
POST /api/conservations/6905a4ba.../messages
{
  "sender": "user",  // ← Ngắn gọn hơn!
  "text": "Hello"
}
```

**Lợi ích:**
- ✅ URL rõ ràng hơn (RESTful)
- ✅ Không cần truyền conversationId trong body
- ✅ Dễ tích hợp với chatbox UI
- ✅ Verify relationship tự động

---

## 🎨 Complete Chatbox Flow:

### **1. Load Conservation & Messages:**

```javascript
// Get conservation với tất cả messages
const response = await fetch(`/api/conservations/${conservationId}/with-messages`);
const data = await response.json();

// data.conservation - Info của conservation
// data.messages - Array of messages
// data.totalMessages - Count

console.log(data);
/*
{
  "conservation": {
    "_id": "...",
    "title": "Chat về Python",
    "messageCount": 5
  },
  "messages": [
    {sender: "system", text: "Chào bạn!"},
    {sender: "user", text: "Xin chào!"},
    ...
  ],
  "totalMessages": 5
}
*/
```

### **2. User gửi message:**

```javascript
async function sendUserMessage(conservationId, text) {
  const response = await fetch(`/api/conservations/${conservationId}/messages`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      sender: 'user',
      text: text
    })
  });
  
  const message = await response.json();
  
  // Add message to UI
  addMessageToUI(message);
  
  return message;
}
```

### **3. System response (AI):**

```javascript
async function sendSystemMessage(conservationId, text) {
  const response = await fetch(`/api/conservations/${conservationId}/messages`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      sender: 'system',
      text: text
    })
  });
  
  return response.json();
}
```

### **4. User xóa message:**

```javascript
async function deleteUserMessage(conservationId, messageId) {
  const response = await fetch(
    `/api/conservations/${conservationId}/messages/${messageId}`,
    {method: 'DELETE'}
  );
  
  if (response.ok) {
    // Remove from UI
    removeMessageFromUI(messageId);
  }
}
```

---

## 🎯 React Component Example:

```jsx
import React, { useState, useEffect } from 'react';

function Chatbox({ conservationId }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  
  // Load messages khi component mount
  useEffect(() => {
    loadConservation();
  }, [conservationId]);
  
  const loadConservation = async () => {
    const response = await fetch(
      `/api/conservations/${conservationId}/with-messages`
    );
    const data = await response.json();
    setMessages(data.messages);
  };
  
  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    
    // Send user message
    const response = await fetch(
      `/api/conservations/${conservationId}/messages`,
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          sender: 'user',
          text: inputText
        })
      }
    );
    
    const newMessage = await response.json();
    
    // Add to UI
    setMessages([...messages, newMessage]);
    setInputText('');
    
    // TODO: Call AI để generate system response
  };
  
  const handleDeleteMessage = async (messageId) => {
    const response = await fetch(
      `/api/conservations/${conservationId}/messages/${messageId}`,
      {method: 'DELETE'}
    );
    
    if (response.ok) {
      // Remove from UI
      setMessages(messages.filter(m => m._id !== messageId));
    }
  };
  
  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map(msg => (
          <div key={msg._id} className={`message ${msg.sender}`}>
            <span>{msg.text}</span>
            {msg.sender === 'user' && (
              <button onClick={() => handleDeleteMessage(msg._id)}>
                Xóa
              </button>
            )}
          </div>
        ))}
      </div>
      
      <div className="input">
        <input
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
        />
        <button onClick={handleSendMessage}>Gửi</button>
      </div>
    </div>
  );
}
```

---

## 🧪 Test với Swagger UI:

Mở: **http://localhost:8000/docs**

Tìm section **"Conservations"**, bạn sẽ thấy:

### **Standard Endpoints:**
- POST `/api/conservations/`
- GET `/api/conservations/{id}`
- GET `/api/conservations/{id}/with-messages`
- etc.

### **Nested Endpoints** ⭐ MỚI:
- POST `/api/conservations/{conservation_id}/messages` 
- DELETE `/api/conservations/{conservation_id}/messages/{message_id}`

---

## 📝 API Reference:

### **POST /api/conservations/{conservation_id}/messages**

**Purpose:** Thêm message vào conservation (dùng cho chatbox)

**Parameters:**
- `conservation_id` (path) - ID của conservation

**Request Body:**
```json
{
  "sender": "user",        // Required: "system" hoặc "user"
  "text": "Hello!",        // Required: Nội dung message
  "type": "text"           // Optional: Default "text"
}
```

**Response:** `201 Created`
```json
{
  "_id": "...",
  "conversationId": "...",
  "sender": "user",
  "text": "Hello!",
  "type": "text",
  "createdAt": "...",
  "updatedAt": "...",
  "__v": 0
}
```

**Errors:**
- `400` - Sender không hợp lệ, text empty, conservation không tồn tại
- `500` - Server error

---

### **DELETE /api/conservations/{conservation_id}/messages/{message_id}**

**Purpose:** Xóa message từ conservation

**Parameters:**
- `conservation_id` (path) - ID của conservation
- `message_id` (path) - ID của message cần xóa
- `update_count` (query) - Update message count (default: true)

**Response:** `200 OK`
```json
{
  "message": "Message đã được xóa khỏi conservation"
}
```

**Errors:**
- `404` - Message không tồn tại
- `400` - Message không thuộc conservation này
- `500` - Server error

**Security:**
- ✅ Verify message thuộc conservation
- ✅ Không thể xóa message của conservation khác

---

## 🎨 Frontend Integration:

### **Vue.js Example:**

```vue
<template>
  <div class="chatbox">
    <div class="messages">
      <div v-for="msg in messages" :key="msg._id" :class="msg.sender">
        {{ msg.text }}
        <button v-if="msg.sender === 'user'" @click="deleteMessage(msg._id)">
          🗑️
        </button>
      </div>
    </div>
    
    <input v-model="newMessage" @keyup.enter="sendMessage" />
    <button @click="sendMessage">Gửi</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      conservationId: '6905a4bada4db5565a169084',
      messages: [],
      newMessage: ''
    }
  },
  
  mounted() {
    this.loadChat();
  },
  
  methods: {
    async loadChat() {
      const res = await fetch(`/api/conservations/${this.conservationId}/with-messages`);
      const data = await res.json();
      this.messages = data.messages;
    },
    
    async sendMessage() {
      if (!this.newMessage.trim()) return;
      
      const res = await fetch(`/api/conservations/${this.conservationId}/messages`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          sender: 'user',
          text: this.newMessage
        })
      });
      
      const newMsg = await res.json();
      this.messages.push(newMsg);
      this.newMessage = '';
    },
    
    async deleteMessage(messageId) {
      const res = await fetch(
        `/api/conservations/${this.conservationId}/messages/${messageId}`,
        {method: 'DELETE'}
      );
      
      if (res.ok) {
        this.messages = this.messages.filter(m => m._id !== messageId);
      }
    }
  }
}
</script>
```

---

## 🔄 Complete Chat Flow:

```
1. User opens chatbox
   ↓
   GET /api/conservations/{id}/with-messages
   ↓
   Load conservation + all messages

2. User types message and clicks "Send"
   ↓
   POST /api/conservations/{id}/messages
   {sender: "user", text: "Hello"}
   ↓
   Message created + messageCount += 1
   ↓
   Display message in UI

3. System generates AI response
   ↓
   POST /api/conservations/{id}/messages
   {sender: "system", text: "Hi there!"}
   ↓
   Message created + messageCount += 1
   ↓
   Display AI response in UI

4. User deletes message
   ↓
   DELETE /api/conservations/{id}/messages/{messageId}
   ↓
   Message deleted + messageCount -= 1
   ↓
   Remove from UI
```

---

## 📊 Endpoints Summary:

### **Conservation Endpoints (9 total):**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/conservations/` | Tạo conservation mới |
| GET | `/api/conservations/{id}` | Get conservation |
| GET | `/api/conservations/{id}/with-messages` | Get với messages |
| GET | `/api/conservations/` | List conservations |
| PUT | `/api/conservations/{id}` | Update conservation |
| POST | `/api/conservations/{id}/facts` | Add fact |
| DELETE | `/api/conservations/{id}` | Delete conservation |
| **POST** | `/api/conservations/{id}/messages` | **Add message** ⭐ |
| **DELETE** | `/api/conservations/{id}/messages/{mid}` | **Remove message** ⭐ |

---

## 🎯 Best Practices:

### **1. Sử dụng Nested Endpoints cho Chatbox:**

✅ **DO:**
```javascript
// Thêm message qua conservation
POST /api/conservations/{id}/messages
```

❌ **DON'T:**
```javascript
// Tạo message riêng lẻ (phức tạp hơn)
POST /api/messages/
{conversationId: "..."}  // Phải nhập conversationId
```

### **2. Load Full Chat:**

✅ **DO:**
```javascript
// Load một lần, có tất cả
GET /api/conservations/{id}/with-messages
```

❌ **DON'T:**
```javascript
// Load riêng (2 requests)
GET /api/conservations/{id}
GET /api/messages/conversation/{id}
```

### **3. Delete Message:**

✅ **DO:**
```javascript
// Nested endpoint - có validation
DELETE /api/conservations/{id}/messages/{messageId}
```

✅ **ALSO OK:**
```javascript
// Direct endpoint - nhanh hơn nhưng ít validation
DELETE /api/messages/{messageId}
```

---

## 🧪 Test với Swagger UI:

Mở: **http://localhost:8000/docs**

### **Test Add Message:**
1. Scroll to **"Conservations"** section
2. Tìm endpoint: **POST /api/conservations/{conservation_id}/messages**
3. Click "Try it out"
4. Nhập:
   - `conservation_id`: `6905a4bada4db5565a169084`
   - Request body:
     ```json
     {
       "sender": "user",
       "text": "Test message from Swagger"
     }
     ```
5. Click "Execute"
6. Xem response!

### **Test Delete Message:**
1. Tìm endpoint: **DELETE /api/conservations/{conservation_id}/messages/{message_id}**
2. Click "Try it out"
3. Nhập conservation_id và message_id
4. Click "Execute"

---

## 🔒 Security Features:

### **Validation khi xóa message:**

```python
# Backend validation
message = message_service.get_by_id(message_id)

if message.conversation_id != conservation_id:
    raise HTTPException(400, "Message không thuộc conservation này")
```

→ Không thể xóa message của conservation khác!

---

## ⚡ Performance Tips:

### **1. Load Chat Efficiently:**

```javascript
// Option 1: Load all (dùng cho small chats)
GET /api/conservations/{id}/with-messages

// Option 2: Load với pagination (dùng cho large chats)
GET /api/conservations/{id}
GET /api/messages/conversation/{id}?page=1&page_size=50
```

### **2. Real-time Updates:**

```javascript
// WebSocket pseudo-code
socket.on('new_message', async (data) => {
  if (data.conservationId === currentConservationId) {
    // Reload messages hoặc append
    messages.push(data.message);
  }
});
```

---

## 📚 API Endpoints Đầy đủ:

### **Conservations:**
```
POST   /api/conservations/
GET    /api/conservations/{id}
GET    /api/conservations/{id}/with-messages
GET    /api/conservations/
PUT    /api/conservations/{id}
POST   /api/conservations/{id}/facts
DELETE /api/conservations/{id}
POST   /api/conservations/{id}/messages          ⭐ NEW
DELETE /api/conservations/{id}/messages/{mid}    ⭐ NEW
```

### **Messages:**
```
POST   /api/messages/
GET    /api/messages/{id}
GET    /api/messages/conversation/{id}
PUT    /api/messages/{id}
DELETE /api/messages/{id}
```

---

## 🎊 Summary:

✅ **2 nested endpoints** cho chatbox  
✅ **Auto message count** update  
✅ **Security validation** (verify ownership)  
✅ **RESTful design** (nested resources)  
✅ **Easy frontend integration**  
✅ **Error handling** complete  

---

## 🚀 Test Ngay:

```bash
# Add message
curl -X POST "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/messages" \
  -H "Content-Type: application/json" \
  -d '{"sender":"user","text":"Test!"}'

# Delete message
curl -X DELETE "http://localhost:8000/api/conservations/6905a4bada4db5565a169084/messages/MESSAGE_ID"
```

**Hoặc test trên Swagger:**
```
http://localhost:8000/docs
```

---

Happy Chatting! 💬✨

