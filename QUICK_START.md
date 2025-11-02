# ⚡ QUICK START - 404 Brain Not Found

## 🎉 Hoàn thành cài đặt!

Tất cả code đã được tạo và test thành công!

---

## 🚀 Chạy ngay (2 bước)

### Bước 1: Chạy Backend (Terminal 1)

```bash
cd "D:\Semester 5\newHackathon\404_Brain_Not_Found"
python -m BE.main
```

✅ Backend chạy tại: **http://localhost:8000**

### Bước 2: Chạy Frontend (Terminal 2)

```bash
cd "D:\Semester 5\newHackathon\404_Brain_Not_Found\FE"
npm run dev
```

✅ Frontend chạy tại: **http://localhost:3000**

---

## 🌐 Truy cập

### Frontend UI
http://localhost:3000

### Backend API Documentation
http://localhost:8000/docs

### API Root Info
http://localhost:8000

---

## 📡 API Endpoints

### ✅ User Management (`/api/users`)
- POST `/api/users/` - Tạo user
- GET `/api/users/{id}` - Lấy user
- GET `/api/users/` - List users

### ✅ AI Services (`/ai`)
- POST `/ai/generate` - Generate code
- POST `/ai/review` - Review code

### ⭐ Agent Orchestration (`/agent`)
- POST `/agent/session/create` - Tạo session
- POST `/agent/context/parse` - Parse context (F1)
- POST `/agent/prompt/process` - Generate với intent (F2)
- POST `/agent/code/analyze` - Analyze code (F3)

---

## 🧪 Test nhanh

### Test Backend
```bash
python test_agent_api.py
```

### Test trong Browser
1. Mở http://localhost:8000/docs
2. Expand "Agent Orchestration"
3. Click "Try it out" và test!

### Test Frontend
1. Mở http://localhost:3000
2. Click "New Chat"
3. Gõ: `Tạo function fibonacci`
4. Bấm Enter hoặc Send
5. Xem AI generate code!

---

## ⚠️ Lưu ý quan trọng

### GEMINI_API_KEY

File `.env` đã được tạo nhưng **chưa có API key thật**.

**Cách lấy API key:**
1. Truy cập: https://makersuite.google.com/app/apikey
2. Tạo API key mới
3. Copy và paste vào `.env`:
   ```env
   GEMINI_API_KEY=AIzaSy...your_key_here
   ```

### Nếu không có API key
Backend vẫn chạy nhưng sẽ **lỗi khi generate code**.

---

## 🎨 Features

### Frontend
- 🌙 Dark/Light theme (màu cam + đen/trắng)
- 💬 Real-time chat UI
- 📝 Code syntax highlighting
- 📋 Copy code button
- 💾 LocalStorage persistence
- 📱 Responsive design

### Backend
- 🤖 AI Code Generation
- 🔍 Code Review
- 🎯 Agent Orchestration
- 📊 Session Management
- 💾 MongoDB persistence
- 📚 Auto documentation (Swagger)

---

## 📊 Thống kê

- ✅ **22 API routes** đã register
- ✅ **8 files mới** đã tạo
- ✅ **3 MongoDB collections**
- ✅ **3 workflows** (F1, F2, F3)

---

## 🆘 Cần giúp đỡ?

Xem các file documentation:
- `SETUP_GUIDE.md` - Hướng dẫn chi tiết
- `BE/AGENT_ORCHESTRATION_GUIDE.md` - API Guide
- `BE/FRONTEND_INTEGRATION.md` - Frontend integration

---

**Chúc bạn demo thành công! 🎉**

