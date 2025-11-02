# ⚡ API Quick Reference

## 🚀 Start Server:

```bash
python -m BE.main
```

Server: **http://localhost:8000**  
Docs: **http://localhost:8000/docs**

---

## 📊 Collections trong MongoDB:

| Collection | Documents | API Endpoint |
|------------|-----------|--------------|
| users | 2 | `/api/users` |
| requests | 3 | `/api/requests` |
| code_generations | 1 | `/api/code-generations` |
| code_reviews | 1 | `/api/code-reviews` |
| execution_logs | 1 | `/api/execution-logs` |
| chat_rooms | 1 | `/api/chat-rooms` |

**Total: 9 documents trong 6 collections**

---

## 🎯 API Endpoints:

### **Users** (7 endpoints)
```http
GET    /api/users/
POST   /api/users/
GET    /api/users/{id}
GET    /api/users/email/{email}
PUT    /api/users/{id}
DELETE /api/users/{id}
```

### **Requests** (4 endpoints)
```http
GET    /api/requests/                    # Lấy tất cả
GET    /api/requests/?user_id=xxx        # Filter by user
GET    /api/requests/?language=Python    # Filter by language
POST   /api/requests/                    # Tạo mới
GET    /api/requests/{id}
DELETE /api/requests/{id}
```

**Request Structure:**
```json
{
  "user_id": "6906ae5b...",
  "requirement_text": "Viết API CRUD...",
  "language": "Python"
}
```

### **Code Generations** (4 endpoints)
```http
GET    /api/code-generations/
GET    /api/code-generations/?request_id=xxx
GET    /api/code-generations/?status=success
POST   /api/code-generations/
GET    /api/code-generations/{id}
DELETE /api/code-generations/{id}
```

**CodeGeneration Structure:**
```json
{
  "request_id": "6906ae76...",
  "files_json": [
    {"filename": "main.py", "content": "..."}
  ],
  "run_instructions": "python main.py",
  "status": "success"
}
```

### **Code Reviews** (4 endpoints)
```http
GET    /api/code-reviews/
GET    /api/code-reviews/?gen_id=xxx
GET    /api/code-reviews/?min_score=7&max_score=10
POST   /api/code-reviews/
GET    /api/code-reviews/{id}
DELETE /api/code-reviews/{id}
```

**CodeReview Structure:**
```json
{
  "gen_id": "6906af32...",
  "review_markdown": "# Review\n- Good code\n- Add validation",
  "score": 8,
  "summary": "Code tốt, cần cải thiện"
}
```

### **Execution Logs** (4 endpoints)
```http
GET    /api/execution-logs/
GET    /api/execution-logs/?gen_id=xxx
POST   /api/execution-logs/
GET    /api/execution-logs/{id}
DELETE /api/execution-logs/{id}
```

**ExecutionLog Structure:**
```json
{
  "gen_id": "6906af32...",
  "compile_result": {"success": true, "output": "OK"},
  "test_result": {"total": 5, "passed": 5, "failed": 0},
  "lint_result": {"issues": 0, "warnings": []}
}
```

### **Chat Rooms** (5 endpoints)
```http
GET    /api/chat-rooms/
GET    /api/chat-rooms/?user_id=xxx
GET    /api/chat-rooms/?active_only=true
POST   /api/chat-rooms/
GET    /api/chat-rooms/{id}
PUT    /api/chat-rooms/{id}
DELETE /api/chat-rooms/{id}
```

**ChatRoom Structure:**
```json
{
  "user_id": "673616a9...",
  "title": "My Chat Room",
  "is_active": true
}
```

---

## 🧪 Quick Test:

### **Test Lấy Danh Sách:**
```bash
# Requests
curl "http://localhost:8000/api/requests/"

# Code Generations
curl "http://localhost:8000/api/code-generations/"

# Code Reviews
curl "http://localhost:8000/api/code-reviews/"

# Execution Logs
curl "http://localhost:8000/api/execution-logs/"

# Chat Rooms
curl "http://localhost:8000/api/chat-rooms/"

# Users
curl "http://localhost:8000/api/users/"
```

### **Test với Browser:**
```
http://localhost:8000/docs
```

---

## 📊 Common Query Params:

Tất cả GET endpoints support:
- `page=1` - Số trang (default: 1)
- `page_size=10` - Items per page (default: 10, max: 100)

Specific filters:
- Requests: `?user_id=xxx`, `?language=Python`
- CodeGenerations: `?request_id=xxx`, `?status=success`
- CodeReviews: `?gen_id=xxx`, `?min_score=7&max_score=10`
- ExecutionLogs: `?gen_id=xxx`
- ChatRooms: `?user_id=xxx`, `?active_only=true`

---

## 🔍 Inspect MongoDB:

```bash
python inspect_collections.py
```

---

## 📚 Full Documentation:

- **`FIXED_ENTITIES_SUMMARY.md`** - Chi tiết changes
- **`ALL_ENTITIES_API_GUIDE.md`** - Complete API guide
- **`BE/ARCHITECTURE.md`** - Architecture details
- **http://localhost:8000/docs** - Live Swagger UI

---

## ✅ Checklist:

- ✅ 6 entities created/fixed
- ✅ Entities khớp với MongoDB structure 100%
- ✅ 28+ endpoints available
- ✅ No linter errors
- ✅ Server running
- ✅ Auto documentation (Swagger)
- ✅ Ready to test!

---

Happy Testing! 🚀

