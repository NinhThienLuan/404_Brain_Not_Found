# 🚀 SETUP GUIDE - Agent Orchestration System

## ✅ Hoàn thành cài đặt

Tất cả code đã được tạo thành công! 

### 📊 Thống kê

- ✅ **8 files mới** đã được tạo
- ✅ **1 file** đã được update (main.py)
- ✅ **22 API routes** đã được register
- ✅ **Dependencies** đã được cài đặt
- ✅ **File .env** đã được tạo

## 📁 Files đã tạo

### Entities (Domain Models)
```
BE/entities/
├── user_entity.py          ✅ CŨ
├── session_entity.py       ✅ MỚI
└── context_entity.py       ✅ MỚI
```

### Pydantic Models (API Contracts)
```
BE/model/
├── ai_models.py                 ✅ CŨ
└── orchestration_models.py      ✅ MỚI
```

### Repositories (Data Access)
```
BE/repository/
├── user_repo.py         ✅ CŨ
├── gemini_repo.py       ✅ CŨ (đã fix import)
├── session_repo.py      ✅ MỚI
└── context_repo.py      ✅ MỚI
```

### Services (Business Logic)
```
BE/service/
├── user_service.py                      ✅ CŨ
├── ai_service.py                        ✅ CŨ (đã fix import)
├── context_parsing_service.py           ✅ MỚI
└── agent_orchestration_service.py       ✅ MỚI
```

### Controllers (API Endpoints)
```
BE/controller/
├── user_controller.py       ✅ CŨ
├── ai_controller.py         ✅ CŨ (đã fix import)
└── agent_controller.py      ✅ MỚI
```

### Main Application
```
BE/main.py                   ✅ UPDATED (đã thêm 2 routers)
```

### Documentation
```
BE/AGENT_ORCHESTRATION_GUIDE.md      ✅ MỚI
BE/FRONTEND_INTEGRATION.md           ✅ MỚI
test_agent_api.py                    ✅ MỚI
.env                                 ✅ MỚI
```

---

## 🎯 API Endpoints đã có

### Group 1: User Management
```
POST   /api/users/              - Tạo user
GET    /api/users/{id}          - Lấy user theo ID
GET    /api/users/              - List users (pagination)
GET    /api/users/email/{email} - Tìm user theo email
PUT    /api/users/{id}          - Update user
PATCH  /api/users/{id}          - Partial update
DELETE /api/users/{id}          - Xóa user
```

### Group 2: AI Services
```
POST   /ai/generate             - Generate code
POST   /ai/review               - Review code
GET    /ai/health               - Health check
```

### Group 3: Agent Orchestration ⭐ NEW
```
POST   /agent/session/create              - Tạo session
GET    /agent/session/{session_id}        - Lấy session info
POST   /agent/context/parse               - Parse context (F1)
POST   /agent/prompt/process              - Generate code với intent (F2)
POST   /agent/code/analyze                - Analyze code (F3)
GET    /agent/health                      - Health check
```

---

## 🚀 Chạy Backend

### Option 1: Chạy thông thường
```bash
cd "D:\Semester 5\newHackathon\404_Brain_Not_Found"
python -m BE.main
```

### Option 2: Chạy với uvicorn trực tiếp
```bash
uvicorn BE.main:app --host 0.0.0.0 --port 8000 --reload
```

Server sẽ chạy tại:
- 🌐 **URL**: http://localhost:8000
- 📚 **Swagger UI**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Test API

### Test tự động
```bash
python test_agent_api.py
```

### Test thủ công với Swagger UI
1. Mở http://localhost:8000/docs
2. Expand section "Agent Orchestration"
3. Test từng endpoint:
   - Create Session
   - Parse Context
   - Process Prompt
   - Analyze Code

### Test bằng cURL

**1. Create Session:**
```bash
curl -X POST http://localhost:8000/agent/session/create \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"user_123\"}"
```

**2. Parse Context (F1):**
```bash
curl -X POST "http://localhost:8000/agent/context/parse?session_id=SESSION_ID&context_text=Tạo API quản lý sản phẩm"
```

**3. Generate Code (F2):**
```bash
curl -X POST http://localhost:8000/agent/prompt/process \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"SESSION_ID\", \"user_id\": \"user_123\", \"prompt\": \"Tạo function thêm sản phẩm\"}"
```

**4. Analyze Code (F3):**
```bash
curl -X POST "http://localhost:8000/agent/code/analyze?session_id=SESSION_ID"
```

---

## 🔗 Kết nối với Frontend

Frontend đang chạy tại: http://localhost:3000

### CORS đã được cấu hình
```python
allow_origins=["*"]  # Chấp nhận tất cả origins
```

### API calls từ FE
```typescript
// Tạo session
const response = await axios.post('http://localhost:8000/agent/session/create', {
  user_id: 'user_123'
});

// Generate code
const codeResponse = await axios.post('http://localhost:8000/agent/prompt/process', {
  session_id: sessionId,
  user_id: 'user_123',
  prompt: 'Tạo function fibonacci'
});
```

---

## ⚙️ Configuration (.env)

File `.env` đã được tạo với config:

```env
APP_PORT=8000
GEMINI_API_KEY=YOUR_API_KEY_HERE  ← ⚠️ CẦN THAY ĐỔI
MONGO_USERNAME=mongo
MONGO_PASSWORD=OtfagZQFKuslkxmpTCZTlvctRGsQBLnk
MONGO_HOST=shortline.proxy.rlwy.net
MONGO_PORT=21101
MONGO_DATABASE=basic-hackathon
```

### ⚠️ QUAN TRỌNG: Thay GEMINI_API_KEY

Lấy API key từ: https://makersuite.google.com/app/apikey

Sau đó update vào file `.env`:
```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

---

## 📊 Database Collections

MongoDB sẽ tự động tạo 3 collections:

### 1. `users` ✅ (đã có)
```javascript
{
  "_id": ObjectId("..."),
  "name": "Nguyễn Văn A",
  "email": "a@example.com",
  "created_at": ISODate("...")
}
```

### 2. `sessions` ⭐ (mới)
```javascript
{
  "_id": ObjectId("..."),
  "user_id": "user_123",
  "current_step": "completed",
  "context_json": {...},
  "code_history": [...],
  "last_intent": "create_new",
  "last_prompt": "...",
  "metadata": {},
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

### 3. `contexts` ⭐ (mới)
```javascript
{
  "_id": ObjectId("..."),
  "session_id": "session_123",
  "raw_text": "Tạo API quản lý sản phẩm...",
  "parsed_json": {...},
  "parsing_model": "gemini-2.5-flash",
  "confidence_score": 0.95,
  "created_at": ISODate("...")
}
```

---

## 🎯 Kiến trúc hoàn chỉnh

```
Frontend (React - Port 3000)
    │
    ├── Chat UI
    ├── Theme Toggle
    └── Message Display
         │
         │ HTTP Requests
         ▼
Backend (FastAPI - Port 8000)
    │
    ├── /api/users/*     → UserController      → UserService
    ├── /ai/*            → AIController        → CodeGenerationService
    └── /agent/*         → AgentController     → AgentOrchestrationService
                                                     │
                                                     ├─► ContextParsingService
                                                     ├─► CodeGenerationService (reuse)
                                                     └─► Gemini AI
         │
         ▼
MongoDB (Railway)
    │
    ├── users collection
    ├── sessions collection
    └── contexts collection
```

---

## 🐛 Troubleshooting

### Lỗi "GEMINI_API_KEY is required"
→ Update API key trong `.env`

### Lỗi "Module not found"
→ Chạy: `pip install -r BE/requirements.txt`

### Lỗi MongoDB connection
→ Check connection string trong `.env`

### Port 8000 đã được sử dụng
→ Đổi `APP_PORT=8001` trong `.env`

---

## ✨ Next Steps

### 1. Chạy Backend
```bash
python -m BE.main
```

### 2. Chạy Frontend (terminal mới)
```bash
cd FE
npm run dev
```

### 3. Test API
```bash
python test_agent_api.py
```

### 4. Mở Swagger UI
http://localhost:8000/docs

---

## 🎉 Hoàn thành!

Bạn đã có:
- ✅ Backend với 3 groups API
- ✅ Agent Orchestration System (F1, F2, F3)
- ✅ Frontend với UI đẹp (màu cam)
- ✅ MongoDB integration
- ✅ Gemini AI integration

**Chúc bạn demo thành công! 🚀**

---

**Team**: 404 Brain Not Found  
**Version**: 2.0.0  
**Date**: 2025-11-02

