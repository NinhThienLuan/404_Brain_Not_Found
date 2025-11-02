# 404_Brain_Not_Found

**FU25 Seal Hackathon**

## 👥 Team Members
- **SE194205** - Ninh Thiện Luân
- **SE181846** - Trương Xuân Nguyên
- **SE190608** - Phan Anh Khoa
- **SE190182** - Mai Nhật Minh
- **SE190302** - Lê Quốc Khánh

## 🤖 Dự án: AI Agent - Code Generation & Review

### 📋 Mô tả
Dự án AI Agent sử dụng Google Gemini API để hỗ trợ:
- 🚀 **Code Generation**: Tự động sinh code dựa trên mô tả yêu cầu
- 🔍 **Code Review**: Phân tích và đánh giá chất lượng code, đưa ra gợi ý cải thiện
- 👥 **User Management**: CRUD API hoàn chỉnh với MongoDB
- 📊 **Tracking & Logging**: Theo dõi requests, executions, reviews

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install email-validator
```

### 2. Start Server
```bash
python -m BE.main
```

Server: **http://localhost:8000**

### 3. Test APIs
Mở browser: **http://localhost:8000/docs**

---

## 📊 API Endpoints

### ✅ 6 Entities với 28+ Endpoints:

| Entity | Endpoint | MongoDB Docs |
|--------|----------|--------------|
| 👥 **Users** | `/api/users` | 2 users sẵn |
| 📝 **Requests** | `/api/requests` | 3 requests sẵn |
| 🚀 **Code Generations** | `/api/code-generations` | 1 generation sẵn |
| 🔍 **Code Reviews** | `/api/code-reviews` | 1 review sẵn |
| 📊 **Execution Logs** | `/api/execution-logs` | 1 log sẵn |
| 💬 **Chat Rooms** | `/api/chat-rooms` | 1 room sẵn |

**Total: 9 documents có sẵn để test!**

---

## 🧪 Testing Tools

### **1. Swagger UI** (Recommended)
```
http://localhost:8000/docs
```

### **2. MongoDB Inspector**
```bash
python inspect_collections.py
```

### **3. API Tester**
```bash
python test_all_apis.py
```

### **4. Postman**
Import: `User_API.postman_collection.json`

---

## 🏗️ Architecture

```
Controller → Service → Repository → Entity → MongoDB
```

**Clean Architecture với:**
- ✅ Entity-based design (Type-safe)
- ✅ Repository pattern (Data access)
- ✅ Service layer (Business logic)
- ✅ Auto documentation (Swagger)

---

## 📚 Documentation

### **Quick Guides:**
- ⚡ **START_HERE.md** - This file
- 📖 **API_QUICK_REFERENCE.md** - API reference
- 🎯 **FINAL_SUMMARY.md** - Complete summary

### **Detailed Docs:**
- 🏗️ **FIXED_ENTITIES_SUMMARY.md** - Entities details
- 📮 **POSTMAN_GUIDE.md** - Postman testing
- 🔍 **MONGODB_INSPECTOR_GUIDE.md** - MongoDB tools
- 📄 **BE/ARCHITECTURE.md** - Architecture deep dive

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern web framework
- **MongoDB** - NoSQL database
- **Pydantic** - Data validation
- **Google Gemini AI** - Code generation/review
- **Clean Architecture** - Entity-based design

---

## 📝 Example Usage

### **Get Requests:**
```bash
curl "http://localhost:8000/api/requests/"
```

**Response:**
```json
{
  "items": [
    {
      "_id": "6906ae76...",
      "user_id": "6906ae5b...",
      "requirement_text": "Viết API CRUD sản phẩm với FastAPI và MongoDB",
      "language": "Python",
      "created_at": "2025-11-02T01:05:58.725Z"
    }
  ],
  "total": 3,
  "page": 1,
  "page_size": 10
}
```

---

## 🎊 Ready to Use!

✅ **Server sẵn sàng**  
✅ **APIs hoạt động**  
✅ **Data có sẵn để test**  
✅ **Documentation đầy đủ**  

**Test ngay:** http://localhost:8000/docs 🚀