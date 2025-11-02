# 🤖 Agent Orchestration System - Hướng dẫn sử dụng

## 📋 Tổng quan

Hệ thống Agent Orchestration cung cấp 3 luồng công việc chính:
- **F1**: Parse Context - Trích xuất JSON từ mô tả text
- **F2**: Process Prompt - Classify intent và generate code
- **F3**: Analyze Code - Phân tích code đã generate

## 🚀 Khởi động

### 1. Chạy Backend
```bash
cd "D:\Semester 5\newHackathon\404_Brain_Not_Found"
python -m BE.main
```

Server chạy tại: **http://localhost:8000**

### 2. Xem API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 API Endpoints

### Group 1: Session Management

#### Tạo Session mới
```http
POST /agent/session/create
Content-Type: application/json

{
  "user_id": "user_123",
  "metadata": {}
}
```

**Response:**
```json
{
  "session_id": "6789abc...",
  "user_id": "user_123",
  "current_step": "idle",
  "context_json": null,
  "code_history": [],
  "created_at": "2025-11-02T10:00:00Z",
  "updated_at": "2025-11-02T10:00:00Z"
}
```

#### Lấy thông tin Session
```http
GET /agent/session/{session_id}
```

### Group 2: Luồng F1 - Parse Context

#### Parse Context Text
```http
POST /agent/context/parse?session_id={id}&context_text={text}&model=gemini-2.5-flash
```

**Ví dụ:**
```http
POST /agent/context/parse?session_id=6789abc&context_text=Tạo API quản lý sản phẩm với CRUD operations, input là tên và giá, output là JSON
```

**Response:**
```json
{
  "session_id": "6789abc...",
  "current_step": "idle",
  "context_json": {
    "topic": "Product Management API",
    "main_function": "CRUD operations",
    "sub_functions": ["Create", "Read", "Update", "Delete"],
    "input_data": "product name, price",
    "output_data": "JSON",
    "technology": "FastAPI",
    "additional_requirements": ["Validation"]
  },
  "success": true,
  "message": "Context parsed successfully (confidence: 0.95)",
  "timestamp": "2025-11-02T10:15:00Z"
}
```

### Group 3: Luồng F2 - Process Prompt

#### Generate Code với Intent Classification
```http
POST /agent/prompt/process
Content-Type: application/json

{
  "session_id": "6789abc...",
  "user_id": "user_123",
  "prompt": "Tạo function để thêm sản phẩm mới",
  "model": "gemini-2.5-flash"
}
```

**Response:**
```json
{
  "session_id": "6789abc...",
  "current_step": "completed",
  "intent": "create_new",
  "generated_code": "def create_product(name: str, price: float):\n    ...",
  "context_json": {...},
  "success": true,
  "message": "Code generated successfully",
  "timestamp": "2025-11-02T10:20:00Z"
}
```

### Group 4: Luồng F3 - Analyze Code

#### Phân tích Code
```http
POST /agent/code/analyze?session_id={id}
```

**Response:**
```json
{
  "session_id": "6789abc...",
  "current_step": "completed",
  "code_analysis": "Function này implement CRUD create operation. Điểm mạnh: clean code, validation. Cần cải thiện: error handling.",
  "success": true,
  "message": "Code analysis completed",
  "timestamp": "2025-11-02T10:25:00Z"
}
```

## 🔄 Workflow hoàn chỉnh

### Ví dụ: Tạo Product Management API

**Bước 1: Tạo Session**
```bash
curl -X POST http://localhost:8000/agent/session/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123"}'
```
→ Nhận `session_id`

**Bước 2: Parse Context (F1)**
```bash
curl -X POST "http://localhost:8000/agent/context/parse?session_id=SESSION_ID&context_text=Tạo API quản lý sản phẩm với CRUD, input tên và giá, output JSON"
```
→ Nhận `context_json`

**Bước 3: Generate Code (F2)**
```bash
curl -X POST http://localhost:8000/agent/prompt/process \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "user_id": "user_123",
    "prompt": "Tạo function thêm sản phẩm"
  }'
```
→ Nhận `generated_code`

**Bước 4: Analyze Code (F3)**
```bash
curl -X POST "http://localhost:8000/agent/code/analyze?session_id=SESSION_ID"
```
→ Nhận `code_analysis`

## 🎯 Workflow States

Session có các state sau:
- `idle` - Đang chờ
- `parsing_context` - Đang parse context
- `classifying_intent` - Đang phân loại intent
- `generating_code` - Đang generate code
- `analyzing_code` - Đang phân tích code
- `completed` - Hoàn thành
- `error` - Có lỗi

## 📊 Database Collections

### Collection: `sessions`
Lưu trữ phiên làm việc của user
- `user_id` - ID của user
- `current_step` - Bước hiện tại
- `context_json` - Context đã parse
- `code_history` - Lịch sử code đã generate
- `last_intent` - Intent cuối cùng
- `last_prompt` - Prompt cuối cùng

### Collection: `contexts`
Lưu trữ context đã được parse
- `session_id` - ID của session
- `raw_text` - Text gốc từ user
- `parsed_json` - JSON đã parse
- `parsing_model` - Model đã sử dụng
- `confidence_score` - Độ tin cậy (0.0-1.0)

## 🔧 Troubleshooting

### Lỗi "Session not found"
→ Tạo session mới với `/agent/session/create`

### Lỗi "No code to analyze"
→ Generate code trước với `/agent/prompt/process`

### Lỗi MongoDB connection
→ Kiểm tra `.env` và connection string

## 🎨 Frontend Integration

Xem file `FRONTEND_INTEGRATION.md` để biết cách tích hợp với React frontend.

## 📚 Tài liệu API đầy đủ

Truy cập http://localhost:8000/docs để xem documentation đầy đủ với Swagger UI.

---

**Version**: 2.0.0  
**Last Updated**: 2025-11-02  
**Team**: 404 Brain Not Found

