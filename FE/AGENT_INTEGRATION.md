# 🔗 Agent Integration - Frontend

## ✅ Đã tích hợp Agent Orchestration

Frontend chatbot đã được tích hợp với **Agent Orchestration System** từ Backend!

---

## 🎯 Features

### 1. **Agent Mode** (Mặc định) ⭐
Sử dụng Agent Orchestration APIs với workflows F1, F2, F3:
- Tự động tạo session khi khởi động
- Classify intent trước khi generate code
- Lưu lịch sử code trong session
- Hỗ trợ parse context và analyze code

### 2. **Fallback Mode**
Nếu Agent session không tạo được, tự động chuyển sang Direct AI mode

---

## 💬 Cách sử dụng

### Gửi prompt thông thường
```
Tạo function để tính fibonacci
```
→ AI sẽ classify intent và generate code (F2)

### Parse Context (F1)
```
/context Tạo API quản lý sản phẩm với CRUD operations, input là tên và giá
```
→ AI sẽ parse text thành JSON structure

### Analyze Code (F3)
```
/analyze
```
→ AI sẽ phân tích code vừa generate

### Review Code
Click nút **🔍 Review Code** → Nhập code → AI review

---

## 🔄 Workflows

### Workflow 1: Generate Code đơn giản
```
User: Tạo function hello world
  ↓
Agent classifies intent: CREATE_NEW
  ↓
Generate code
  ↓
Display: Intent + Code
```

### Workflow 2: Parse Context trước
```
User: /context Tạo API user management với CRUD
  ↓
Parse context → JSON structure
  ↓
User: Tạo function thêm user
  ↓
Generate code (với context)
  ↓
Display: Code với context awareness
```

### Workflow 3: Full workflow
```
1. /context Mô tả project
2. Tạo function X
3. /analyze
4. Review code (button)
```

---

## 🎨 UI Components

### Buttons trong Header
- **📊 Analyze Code** - Phân tích code vừa generate (chỉ hiện khi có Agent session)
- **🔍 Review Code** - Review code tùy chỉnh
- **🌙/☀️ Theme** - Chuyển Dark/Light mode

### Welcome Message
Hiển thị hướng dẫn sử dụng khi Agent Mode active:
```
🤖 AI Agent Mode đã kích hoạt!

💬 Gõ prompt để generate code
📝 /context <text> để parse context
📊 /analyze để phân tích code
🔍 Hoặc click Review Code để review

Session: 6789abc...
```

---

## 🔌 API Calls

### Khi Component Mount
```typescript
POST /agent/session/create
{
  user_id: "user_1730123456",
  metadata: { source: "frontend_chatbot" }
}
```

### Khi gửi prompt thông thường
```typescript
POST /agent/prompt/process
{
  session_id: "...",
  user_id: "...",
  prompt: "Tạo function fibonacci",
  model: "gemini-2.5-flash"
}
```

### Khi gửi /context
```typescript
POST /agent/context/parse?session_id=...&context_text=...&model=gemini-2.5-flash
```

### Khi gửi /analyze
```typescript
POST /agent/code/analyze?session_id=...
```

### Khi click Review Code
```typescript
POST /ai/review
{
  code: "...",
  language: "python",
  review_type: "general"
}
```

---

## 💾 State Management

### Agent State
```typescript
const [agentSessionId, setAgentSessionId] = useState<string | null>(null);
const [useAgentMode, setUseAgentMode] = useState(true);
```

### localStorage
- `userId` - User ID cho Agent session
- `conversations` - Danh sách conversations
- `messages_{convId}` - Messages của từng conversation
- `theme` - Dark/Light mode preference

---

## 🔄 Auto-Fallback

Nếu Agent session tạo thất bại:
```typescript
try {
  // Create agent session
  setAgentSessionId(response.data.session_id);
} catch (err) {
  // Fallback to direct AI
  setUseAgentMode(false);
}
```

Khi `useAgentMode = false`:
- Vẫn có thể chat
- Gọi trực tiếp `/ai/generate` thay vì `/agent/prompt/process`
- Không có session management

---

## 📊 Advantages của Agent Mode

### vs Direct AI Mode

| Feature | Agent Mode | Direct AI |
|---------|-----------|-----------|
| Intent Classification | ✅ Yes | ❌ No |
| Session Management | ✅ Yes | ❌ No |
| Code History | ✅ Saved in DB | ❌ Local only |
| Context Parsing | ✅ F1 workflow | ❌ No |
| Code Analysis | ✅ F3 workflow | ❌ Manual |
| State Tracking | ✅ Workflow steps | ❌ No |

---

## 🐛 Debugging

### Check Agent Session
Mở Browser Console:
```javascript
// Check if agent session created
console.log(localStorage.getItem('userId'));

// Check session in backend
fetch('http://localhost:8000/agent/session/SESSION_ID')
  .then(r => r.json())
  .then(console.log);
```

### Monitor API Calls
Browser DevTools → Network tab → Filter: `/agent/`

---

## ⚙️ Configuration

### API Base URL
```typescript
const API_BASE_URL = "http://localhost:8000";
```

### Agent Mode Toggle
```typescript
const [useAgentMode, setUseAgentMode] = useState(true);  // true = Agent, false = Direct
```

---

## 🎉 Hoàn thành!

Frontend đã được tích hợp đầy đủ với:
- ✅ Agent Orchestration (F1, F2, F3)
- ✅ Direct AI (fallback)
- ✅ Session management
- ✅ Commands support
- ✅ Auto session creation
- ✅ UI enhancements

**Chạy và test ngay!** 🚀

