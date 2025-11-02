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

### 🏗️ Kiến trúc dự án

```
404_Brain_Not_Found/
├── BE/                          # Backend (Python Flask)
│   ├── controller/              # API Controllers
│   │   ├── ai_controller.py     # AI endpoints
│   │   └── hellocontroller.py   # Test controller
│   ├── model/                   # Data Models
│   │   ├── ai_models.py         # AI request/response models
│   │   └── data_models.py       # Database models
│   ├── repo/                    # Repository Layer
│   │   └── gemini_repo.py       # Gemini API integration
│   ├── service/                 # Business Logic
│   │   └── ai_service.py        # AI services
│   ├── utils/                   # Utilities
│   │   └── config.py            # Configuration helpers
│   ├── tests/                   # Unit tests
│   ├── app.py                   # Main application
│   └── requirements.txt         # Python dependencies
├── FE/                          # Frontend (Coming soon)
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

### 🚀 Cài đặt và Chạy

#### 1. Clone repository
```bash
git clone https://github.com/NinhThienLuan/404_Brain_Not_Found.git
cd 404_Brain_Not_Found
```

#### 2. Cài đặt Python dependencies
```bash
cd BE
pip install -r requirements.txt
```

#### 3. Cấu hình Environment Variables
```bash
# Copy file .env.example thành .env
cp ../.env.example .env

# Chỉnh sửa .env và thêm Gemini API key của bạn
# GEMINI_API_KEY=your_actual_api_key_here
```

#### 4. Lấy Gemini API Key
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập bằng Google Account
3. Tạo API Key mới
4. Copy và paste vào file `.env`

#### 5. Chạy ứng dụng
```bash
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

### 📡 API Endpoints

#### 1. Health Check
```
GET /api/ai/health
```

#### 2. Generate Code
```
POST /api/ai/generate
Content-Type: application/json

{
  "prompt": "Create a Python function to calculate fibonacci sequence",
  "language": "python",
  "framework": "flask",
  "additional_context": "Use recursion with memoization"
}
```

**Response:**
```json
{
  "generated_code": "...",
  "explanation": "...",
  "language": "python",
  "timestamp": "2025-11-02T...",
  "success": true
}
```

#### 3. Review Code
```
POST /api/ai/review
Content-Type: application/json

{
  "code": "def fibonacci(n):\n    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
  "language": "python",
  "review_type": "performance",
  "additional_notes": "Focus on optimization"
}
```

**Response:**
```json
{
  "overall_score": 7.5,
  "issues": [...],
  "summary": "...",
  "improvements": [...],
  "timestamp": "2025-11-02T...",
  "success": true
}
```

### 🧪 Testing

```bash
# Chạy tất cả tests
python -m unittest discover tests

# Chạy test cụ thể
python -m unittest tests.test_hellocontroller
```

### 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- Flask (Web Framework)
- Google Generative AI (Gemini)
- python-dotenv (Environment management)

**Frontend:** (Coming soon)
- React/Vue.js
- TailwindCSS

### 📝 Development Workflow

1. **Branch naming**: `feature/feature-name` hoặc `fix/bug-name`
2. **Commit messages**: Sử dụng conventional commits
   - `feat:` cho tính năng mới
   - `fix:` cho bug fixes
   - `docs:` cho documentation
   - `refactor:` cho code refactoring

### 🤝 Contributing

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

### 📄 License

This project is created for FU25 Seal Hackathon.

### 📧 Contact

Nếu có câu hỏi, liên hệ team qua GitHub Issues.

---

**Happy Coding! 🚀**
