# AI Chatbot - Frontend

Ứng dụng chatbot với giao diện đẹp mắt, hiệu ứng không gian vũ trụ và tích hợp Socket.IO để real-time messaging.

## ✨ Tính năng

- 🌌 Giao diện không gian vũ trụ với hiệu ứng động
- 💬 Real-time messaging qua Socket.IO
- 🎨 Dark/Light theme toggle
- 📝 Hỗ trợ hiển thị code blocks với syntax highlighting
- 📁 Import file (txt, pdf, doc, docx, json)
- 🎯 Quản lý nhiều cuộc trò chuyện
- 📱 Responsive design

## 🚀 Cài đặt

### Yêu cầu

- Node.js (v16 trở lên)
- npm hoặc yarn

### Cài đặt dependencies

```bash
npm install
```

## 🎯 Chạy ứng dụng

### Development Mode

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: `http://localhost:5173` (hoặc port khác nếu Vite tự động chọn)

### Build Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 🔧 Cấu hình

### Backend API

Ứng dụng mặc định kết nối tới backend tại: `http://localhost:8080`

Để thay đổi, chỉnh sửa URL trong file `chatbot.tsx`:

```typescript
const newSocket = io("http://localhost:8080"); // Thay đổi URL ở đây
```

### Endpoints API

- `GET /api/conversations` - Lấy danh sách cuộc trò chuyện
- `POST /api/conversations` - Tạo cuộc trò chuyện mới
- `GET /api/messages/:conversationId` - Lấy tin nhắn của cuộc trò chuyện
- `POST /api/conversations/:conversationId/figma-layout` - Tạo layout Figma

### Socket.IO Events

- `connect` - Kết nối thành công
- `join_room` - Tham gia room cuộc trò chuyện
- `send_message` - Gửi tin nhắn
- `receive_message` - Nhận tin nhắn từ AI
- `error` - Xử lý lỗi

## 📦 Dependencies chính

- **React 18** - UI library
- **TypeScript** - Type safety
- **Socket.IO Client** - Real-time communication
- **Axios** - HTTP client
- **Vite** - Build tool & dev server

## 🎨 Themes

Ứng dụng hỗ trợ 2 theme:
- **Dark Mode** (mặc định) - Giao diện tối với hiệu ứng không gian
- **Light Mode** - Giao diện sáng với hiệu ứng nhẹ nhàng

Theme được lưu trong localStorage và tự động áp dụng khi tải lại trang.

## 📁 Cấu trúc file

```
FE/
├── chatbot.tsx          # Component chính
├── chatbot.css          # Styles với theme support
├── main.tsx             # Entry point
├── index.html           # HTML template
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies
```

## 🐛 Xử lý lỗi

### Lỗi kết nối Socket.IO

Nếu không kết nối được Socket.IO, kiểm tra:
1. Backend đã chạy chưa
2. URL Socket.IO có đúng không
3. CORS configuration ở backend

### Lỗi TypeScript

Nếu gặp lỗi TypeScript, chạy:
```bash
npm install --save-dev @types/node @types/react @types/react-dom
```

## 🔒 Bảo mật

- XSS protection qua `escapeHtml` function
- HTML sanitization cho messages
- CORS cần được cấu hình đúng ở backend

## 📝 License

MIT License

## 👥 Contributors

404 Brain Not Found Team

