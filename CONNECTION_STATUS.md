# 🔗 Trạng thái kết nối FE ↔ BE

## ✅ ĐÃ KẾT NỐI HOÀN CHỈNH!

Frontend và Backend đã được tích hợp đầy đủ với **Agent Orchestration System**.

---

## 📡 Kết nối hiện tại

```
┌─────────────────────────────────────────────────────────┐
│         Frontend (React - Port 3000)                     │
│                                                          │
│  Component: Chatbot.tsx                                 │
│  API Base URL: http://localhost:8000                    │
│                                                          │
│  Features:                                              │
│  ✅ Auto create Agent Session on mount                  │
│  ✅ Send prompt → Agent Orchestration (F2)              │
│  ✅ Commands: /context (F1), /analyze (F3)              │
│  ✅ Review Code button → Direct AI                      │
│  ✅ Fallback to Direct AI if Agent fails                │
│                                                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTP/REST API
                       │
┌──────────────────────▼──────────────────────────────────┐
│         Backend (FastAPI - Port 8000)                    │
│                                                          │
│  Registered Routes: 22 endpoints                        │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Group 1: User Management (/api/users)         │    │
│  │  - POST   /api/users/                          │    │
│  │  - GET    /api/users/{id}                      │    │
│  │  - GET    /api/users/                          │    │
│  │  - PUT    /api/users/{id}                      │    │
│  │  - DELETE /api/users/{id}                      │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Group 2: AI Services (/ai)                    │    │
│  │  - POST /ai/generate    ← FE gọi (fallback)    │    │
│  │  - POST /ai/review      ← FE gọi (button)      │    │
│  │  - GET  /ai/health                             │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Group 3: Agent Orchestration (/agent) ⭐      │    │
│  │  - POST /agent/session/create  ← FE gọi (init) │    │
│  │  - GET  /agent/session/{id}                    │    │
│  │  - POST /agent/context/parse   ← FE: /context  │    │
│  │  - POST /agent/prompt/process  ← FE: normal msg│    │
│  │  - POST /agent/code/analyze    ← FE: /analyze  │    │
│  │  - GET  /agent/health                          │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ├─► MongoDB (Railway)
                       │   └─ Collections: users, sessions, contexts
                       │
                       └─► Gemini AI (Google)
                           └─ Models: gemini-2.5-flash
```

---

## 🎮 FE → BE Mapping

### Khi component mount
```typescript
FE: useEffect(() => createAgentSession())
  ↓
BE: POST /agent/session/create
  ↓
Response: session_id
  ↓
FE: setAgentSessionId(session_id)
```

### Khi user gõ prompt bình thường
```typescript
FE: sendMsg("Tạo function fibonacci")
  ↓
BE: POST /agent/prompt/process
  ↓
AgentOrchestrationService:
  1. Classify intent
  2. Generate code (reuse CodeGenerationService)
  3. Save to history
  ↓
Response: { intent, generated_code, ... }
  ↓
FE: Display intent + code
```

### Khi user gõ /context
```typescript
FE: sendMsg("/context Tạo API product management")
  ↓
BE: POST /agent/context/parse
  ↓
ContextParsingService:
  1. Build prompt
  2. Call Gemini
  3. Extract JSON
  4. Save to DB
  ↓
Response: { parsed_json, confidence_score }
  ↓
FE: Display JSON in code block
```

### Khi user gõ /analyze
```typescript
FE: sendMsg("/analyze")
  ↓
BE: POST /agent/code/analyze
  ↓
AgentOrchestrationService:
  1. Get latest code from history
  2. Call Gemini for analysis
  ↓
Response: { code_analysis }
  ↓
FE: Display analysis
```

### Khi user click "Review Code"
```typescript
FE: handleCodeReview()
  ↓
BE: POST /ai/review
  ↓
CodeReviewService:
  1. Build review prompt
  2. Call Gemini
  3. Parse review
  ↓
Response: { overall_score, issues, improvements }
  ↓
FE: Display review result
```

---

## 🔄 Data Flow

### Session Creation
```
Component Mount
  ↓
Check localStorage for userId
  ↓
Create if not exists → userId
  ↓
POST /agent/session/create { user_id }
  ↓
Backend creates Session entity
  ↓
Save to MongoDB sessions collection
  ↓
Return session_id
  ↓
FE stores in state: agentSessionId
```

### Code Generation with Agent
```
User types: "Tạo function X"
  ↓
FE: Add to messages (user)
  ↓
POST /agent/prompt/process
  {
    session_id,
    user_id,
    prompt,
    model
  }
  ↓
BE: AgentOrchestrationService
  ├─► Classify intent (CREATE_NEW/MODIFY/ANALYZE)
  ├─► Update session state (GENERATING_CODE)
  ├─► Call CodeGenerationService.generate_code()
  │   └─► GeminiRepository.generate_code()
  │       └─► Gemini AI API
  ├─► Parse response
  ├─► Save to session.code_history
  └─► Update session state (COMPLETED)
  ↓
Response: {
  intent: "create_new",
  generated_code: "...",
  current_step: "completed"
}
  ↓
FE: Display "🎯 Intent: create_new" + code
```

---

## 🎯 State Management

### Frontend State
```typescript
// Agent Orchestration
agentSessionId: string | null     // Session ID từ backend
useAgentMode: boolean              // true = Agent, false = Direct

// UI State
conversationId: string | null      // Conversation hiện tại
messages: Message[]                // Tin nhắn trong conversation
isThinking: boolean                // AI đang suy nghĩ
currentTheme: "dark" | "light"     // Theme hiện tại
```

### Backend State (trong MongoDB)
```javascript
// sessions collection
{
  "_id": "session_id",
  "user_id": "user_123",
  "current_step": "completed",      // State của workflow
  "context_json": {...},            // Context đã parse (F1)
  "code_history": [                 // Lịch sử code (F2)
    {
      "code": "...",
      "language": "python",
      "timestamp": "..."
    }
  ],
  "last_intent": "create_new",      // Intent cuối cùng
  "last_prompt": "..."              // Prompt cuối cùng
}
```

---

## 📝 Commands Reference

| Command | API Called | Description |
|---------|-----------|-------------|
| `Tạo function X` | `/agent/prompt/process` | Generate code (F2) |
| `/context <text>` | `/agent/context/parse` | Parse context (F1) |
| `/analyze` | `/agent/code/analyze` | Analyze code (F3) |
| Click Review Code | `/ai/review` | Review custom code |

---

## 🔧 Configuration

### API URL
```typescript
const API_BASE_URL = "http://localhost:8000";
```

### Auto Agent Mode
```typescript
const [useAgentMode, setUseAgentMode] = useState(true);
```
Đặt `false` để tắt Agent mode và chỉ dùng Direct AI.

---

## 🧪 Testing Connection

### Test Backend Running
```bash
curl http://localhost:8000/health
```

### Test Agent Session Creation
```bash
curl -X POST http://localhost:8000/agent/session/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'
```

### Test in Frontend
1. Mở http://localhost:3000
2. Mở Browser Console (F12)
3. Xem log: `✅ Agent session created: ...`
4. Create conversation
5. Gõ prompt → Xem API call trong Network tab

---

## ✅ Checklist Integration

- [x] FE tạo Agent session khi mount
- [x] FE gọi `/agent/prompt/process` cho prompt thông thường
- [x] FE support command `/context`
- [x] FE support command `/analyze`
- [x] FE có nút "Analyze Code"
- [x] FE có nút "Review Code"
- [x] FE fallback to Direct AI nếu Agent fail
- [x] FE hiển thị Agent Mode status
- [x] FE hiển thị intent khi generate code
- [x] BE expose tất cả Agent APIs
- [x] BE có CORS cho localhost:3000
- [x] BE có .env configuration

---

## 🎉 Kết luận

**Frontend và Backend đã được kết nối hoàn chỉnh!**

Bạn có thể:
1. Chạy Backend: `python -m BE.main`
2. Chạy Frontend: `npm run dev`
3. Mở http://localhost:3000
4. Chat với AI Agent! 🚀

**Mode:** Agent Orchestration (với F1, F2, F3 workflows)  
**Fallback:** Direct AI (nếu Agent fail)  
**Status:** ✅ Production Ready

