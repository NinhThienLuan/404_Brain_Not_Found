# 🔗 Frontend Integration Guide

## 📦 Cài đặt Dependencies (FE)

```bash
cd FE
npm install axios
```

## 🎯 Tích hợp với Chatbot Component

### Cập nhật `FE/chatbot.tsx`

Thêm các functions sau vào component:

```typescript
// API Base URL
const API_BASE_URL = "http://localhost:8000";

// ==================== SESSION MANAGEMENT ====================

const [sessionId, setSessionId] = useState<string | null>(null);

// Tạo session khi component mount
useEffect(() => {
  const initSession = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/agent/session/create`, {
        user_id: "user_frontend_" + Date.now(),
        metadata: {}
      });
      setSessionId(response.data.session_id);
      console.log("✅ Session created:", response.data.session_id);
    } catch (err) {
      console.error("❌ Error creating session:", err);
    }
  };
  
  initSession();
}, []);

// ==================== FLOW 1: PARSE CONTEXT ====================

const parseContext = async (contextText: string) => {
  if (!sessionId) {
    alert("Session chưa được tạo!");
    return;
  }
  
  setIsThinking(true);
  addMessage(`Đang parse context: ${contextText}`, "user");
  
  try {
    const response = await axios.post(
      `${API_BASE_URL}/agent/context/parse`,
      null,
      {
        params: {
          session_id: sessionId,
          context_text: contextText,
          model: "gemini-2.5-flash"
        }
      }
    );
    
    if (response.data.success) {
      const result = `✅ Context parsed successfully!\n\nConfidence: ${response.data.confidence_score}\n\nParsed JSON:\n\`\`\`json\n${JSON.stringify(response.data.context_json, null, 2)}\n\`\`\``;
      addMessage(result, "system");
    } else {
      addMessage(`❌ Parse failed: ${response.data.error_message}`, "system");
    }
  } catch (err: any) {
    console.error("❌ Error parsing context:", err);
    addMessage(`❌ Error: ${err.message}`, "system");
  } finally {
    setIsThinking(false);
  }
};

// ==================== FLOW 2: PROCESS PROMPT ====================

const processPrompt = async (prompt: string) => {
  if (!sessionId) {
    alert("Session chưa được tạo!");
    return;
  }
  
  setIsThinking(true);
  addMessage(prompt, "user");
  
  try {
    const response = await axios.post(`${API_BASE_URL}/agent/prompt/process`, {
      session_id: sessionId,
      user_id: "user_frontend",
      prompt: prompt,
      model: "gemini-2.5-flash"
    });
    
    if (response.data.success) {
      const result = `🎯 Intent: ${response.data.intent}\n\n📝 Generated Code:\n\`\`\`python\n${response.data.generated_code}\n\`\`\``;
      addMessage(result, "system");
    } else {
      addMessage(`❌ Failed: ${response.data.error_message}`, "system");
    }
  } catch (err: any) {
    console.error("❌ Error processing prompt:", err);
    addMessage(`❌ Error: ${err.message}`, "system");
  } finally {
    setIsThinking(false);
  }
};

// ==================== FLOW 3: ANALYZE CODE ====================

const analyzeCode = async () => {
  if (!sessionId) {
    alert("Session chưa được tạo!");
    return;
  }
  
  setIsThinking(true);
  addMessage("Phân tích code...", "user");
  
  try {
    const response = await axios.post(
      `${API_BASE_URL}/agent/code/analyze`,
      null,
      {
        params: {
          session_id: sessionId
        }
      }
    );
    
    if (response.data.success) {
      const result = `📊 Code Analysis:\n\n${response.data.code_analysis}`;
      addMessage(result, "system");
    } else {
      addMessage(`❌ Failed: ${response.data.error_message}`, "system");
    }
  } catch (err: any) {
    console.error("❌ Error analyzing code:", err);
    addMessage(`❌ Error: ${err.message}`, "system");
  } finally {
    setIsThinking(false);
  }
};

// ==================== UPDATE SEND MESSAGE ====================

const sendMsg = async () => {
  const text = msgInput.trim();
  if (!text || !sessionId) return;
  
  setMsgInput("");
  
  // Detect command type
  if (text.toLowerCase().startsWith("/context ")) {
    // Parse context
    const contextText = text.substring(9);
    await parseContext(contextText);
  } else if (text.toLowerCase() === "/analyze") {
    // Analyze code
    await analyzeCode();
  } else {
    // Normal prompt - generate code
    await processPrompt(text);
  }
  
  // Focus back to input
  setTimeout(() => {
    messageInputRef.current?.focus();
  }, 100);
};
```

## 🎮 Commands trong Chat

User có thể sử dụng các commands:

| Command | Mô tả | Ví dụ |
|---------|-------|-------|
| `/context <text>` | Parse context (F1) | `/context Tạo API quản lý sản phẩm` |
| `<normal text>` | Generate code (F2) | `Tạo function thêm sản phẩm` |
| `/analyze` | Analyze code (F3) | `/analyze` |

## 📝 Ví dụ sử dụng

### Workflow hoàn chỉnh

1. **User gửi context:**
   ```
   /context Tạo API quản lý sản phẩm với CRUD operations. Input: tên, giá. Output: JSON
   ```
   → System parse và hiển thị JSON

2. **User gửi prompt:**
   ```
   Tạo function để thêm sản phẩm mới
   ```
   → System generate code

3. **User phân tích:**
   ```
   /analyze
   ```
   → System phân tích code vừa generate

## 🎨 UI Updates

Thêm buttons trong chat header:

```tsx
<div className="chat-header">
  <span>{currentTitle || "AI Agent - 404 Brain Not Found"}</span>
  <div style={{ display: "flex", gap: "10px", alignItems: "center", marginLeft: "auto" }}>
    {sessionId && (
      <>
        <button onClick={() => {
          const ctx = prompt("Nhập context:");
          if (ctx) parseContext(ctx);
        }}>
          📋 Parse Context
        </button>
        <button onClick={analyzeCode}>
          🔍 Analyze Code
        </button>
      </>
    )}
    <button id="themeToggle" onClick={toggleTheme}>
      {currentTheme === "dark" ? "🌙 Dark" : "☀️ Light"}
    </button>
  </div>
</div>
```

## 🔄 State Management

Session được lưu trong state:
```typescript
const [sessionId, setSessionId] = useState<string | null>(null);
const [contextParsed, setContextParsed] = useState<any>(null);
```

## 📊 Monitoring

Theo dõi workflow state trong console:
```typescript
useEffect(() => {
  if (sessionId) {
    // Periodically check session state
    const interval = setInterval(async () => {
      const response = await axios.get(`${API_BASE_URL}/agent/session/${sessionId}`);
      console.log("Session state:", response.data.current_step);
    }, 5000);
    
    return () => clearInterval(interval);
  }
}, [sessionId]);
```

## 🚨 Error Handling

```typescript
try {
  const response = await axios.post(...);
  if (response.data.success) {
    // Success
  } else {
    // Handle business error
    alert(response.data.error_message);
  }
} catch (err: any) {
  // Handle network/system error
  console.error(err);
  alert("Lỗi kết nối!");
}
```

## 🎯 Best Practices

1. **Luôn tạo session trước khi sử dụng**
2. **Check sessionId trước khi gọi API**
3. **Parse context trước khi generate code** (optional nhưng recommended)
4. **Analyze code sau khi generate** để có feedback
5. **Handle errors gracefully**

## 📱 Testing

### Test trong Browser Console

```javascript
// Create session
const session = await fetch('http://localhost:8000/agent/session/create', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({user_id: 'test_user'})
}).then(r => r.json());

console.log('Session ID:', session.session_id);

// Parse context
const parseResult = await fetch(
  `http://localhost:8000/agent/context/parse?session_id=${session.session_id}&context_text=Tạo API quản lý sản phẩm`
).then(r => r.json());

console.log('Parsed:', parseResult);
```

---

**Happy Coding! 🚀**

