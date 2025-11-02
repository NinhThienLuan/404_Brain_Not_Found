# 🚀 Quick Start - Intent Classifier Service

## Bắt Đầu Nhanh trong 3 Bước

### Bước 1: Cấu Hình Environment

Đảm bảo file `.env` có các biến sau:

```env
GEMINI_API_KEY=AIzaSyAU-sSZj_wKDPyxOvWo1wEHnJqGJ06yCmw
MONGODB_URI=mongodb://mongo:OtfagZQFKuslkxmpTCZTlvctRGsQBLnk@shortline.proxy.rlwy.net:21101
APP_PORT=8080
GEMINI_MODEL=gemini-1.5-flash
```

### Bước 2: Chạy Server

```bash
cd BE
python app.py
```

Hoặc:

```bash
python BE/app.py
```

Server sẽ chạy tại: `http://localhost:8080`

### Bước 3: Test API

#### Option 1: Sử dụng API Docs (Khuyến Nghị)

Mở browser và truy cập:
```
http://localhost:8080/api/docs
```

Tại đây bạn có thể:
- Xem tất cả endpoints
- Test trực tiếp từ browser
- Xem request/response examples

#### Option 2: Sử dụng cURL

```bash
# 1. Health check
curl http://localhost:8080/api/intent/health

# 2. Lấy danh sách intent types
curl http://localhost:8080/api/intent/types

# 3. Phân loại intent cho conservation (thay your_conservation_id)
curl -X POST http://localhost:8080/api/intent/classify/conservation \
  -H "Content-Type: application/json" \
  -d "{\"conservation_id\": \"your_conservation_id\"}"
```

#### Option 3: Sử dụng Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8080/api/intent"

# 1. Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. Get intent types
response = requests.get(f"{BASE_URL}/types")
print(response.json())

# 3. Classify conservation intent
response = requests.post(f"{BASE_URL}/classify/conservation", json={
    "conservation_id": "your_conservation_id",
    "model_name": "gemini-1.5-flash"
})
print(response.json())

# 4. Extract context
response = requests.post(f"{BASE_URL}/context/extract", json={
    "conservation_id": "your_conservation_id"
})
print(response.json())

# 5. Suggest next action
response = requests.post(f"{BASE_URL}/next-action", json={
    "conservation_id": "your_conservation_id",
    "current_intent": "GENERATE_CODE"
})
print(response.json())
```

## 📋 Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/intent/health` | GET | Health check |
| `/api/intent/types` | GET | Get supported intent types |
| `/api/intent/classify/conservation` | POST | Classify conservation intent |
| `/api/intent/classify/message` | POST | Classify single message intent |
| `/api/intent/context/extract` | POST | Extract context from conservation |
| `/api/intent/next-action` | POST | Suggest next action |

## 🎯 7 Intent Types

1. **GENERATE_CODE** - Tạo code mới
2. **REVIEW_CODE** - Review code
3. **EXPLAIN_CODE** - Giải thích code
4. **FIX_ERROR** - Sửa lỗi
5. **REFACTOR** - Tái cấu trúc code
6. **QUESTION** - Câu hỏi chung
7. **CLARIFICATION** - Làm rõ yêu cầu

## 💡 Ví Dụ Response

### Classify Intent Response
```json
{
    "success": true,
    "data": {
        "intent": "GENERATE_CODE",
        "confidence": 0.9,
        "context": {
            "language": "Python",
            "framework": "FastAPI",
            "main_topic": "CRUD API",
            "specific_request": "Tạo CRUD endpoints cho User"
        },
        "suggestion": "Bắt đầu generate code cho CRUD endpoints",
        "requires_clarification": false,
        "conservation_id": "abc123",
        "conservation_title": "Tạo User API",
        "conservation_goal": "Generate FastAPI CRUD",
        "message_count": 3,
        "timestamp": "2024-01-01T00:00:00"
    }
}
```

### Extract Context Response
```json
{
    "success": true,
    "conservation_id": "abc123",
    "data": {
        "key_points": [
            "Tạo CRUD API cho User entity",
            "Sử dụng FastAPI framework",
            "Database: MongoDB"
        ],
        "requirements": [
            "Create endpoint",
            "Read endpoint",
            "Update endpoint",
            "Delete endpoint"
        ],
        "questions": [
            "Cần validate email không?",
            "Password có hash không?"
        ],
        "code_snippets": [],
        "technical_terms": [
            "FastAPI",
            "MongoDB",
            "CRUD",
            "REST API"
        ]
    }
}
```

### Next Action Response
```json
{
    "success": true,
    "conservation_id": "abc123",
    "data": {
        "action": "GENERATE",
        "reasoning": "User đã cung cấp đủ thông tin để bắt đầu generate code",
        "questions_to_ask": [],
        "confidence": 0.85
    }
}
```

## 🧪 Run Tests

Test service với mock data:

```bash
cd BE
python test_intent_service.py
```

Output sẽ hiển thị kết quả của 5 test cases.

## 📚 Documentation

Chi tiết đầy đủ trong:
- `BE/INTENT_CLASSIFIER_README.md` - Full documentation
- `BE/INTENT_CLASSIFIER_SUMMARY.md` - Implementation summary

## ⚠️ Lưu Ý

1. **Conservation ID**: Cần có conservation ID thực tế từ MongoDB để test classify
2. **API Key**: Đảm bảo GEMINI_API_KEY hợp lệ
3. **Messages**: Conservation phải có ít nhất 1 message để phân tích
4. **Model Name**: Có thể bỏ qua, mặc định sẽ dùng gemini-1.5-flash

## 🔧 Troubleshooting

### Lỗi: "Conservation không tồn tại"
→ Kiểm tra conservation_id có đúng không

### Lỗi: "Không có messages để phân tích"
→ Đảm bảo conservation có messages

### Lỗi: Gemini API error
→ Kiểm tra GEMINI_API_KEY và API quota

### Low confidence scores
→ Messages quá ngắn, cần thêm context

## 🎉 Done!

Bây giờ bạn có thể:
- ✅ Phân loại intent của user
- ✅ Trích xuất context từ conversation
- ✅ Đề xuất hành động tiếp theo
- ✅ Guide conversation flow intelligently

Happy coding! 🚀
