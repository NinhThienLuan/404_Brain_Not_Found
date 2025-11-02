"""
Test script cho Chat API
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api/chat"

# Test user ID (thay bằng user ID thực tế từ database)
TEST_USER_ID = "507f1f77bcf86cd799439011"


def print_response(title, response):
    """Helper để in response đẹp"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_chat_api():
    """Test các chức năng của Chat API"""
    
    print("\n🚀 Bắt đầu test Chat API...")
    
    # 1. Tạo phòng chat mới
    print("\n\n1️⃣ TEST: Tạo phòng chat mới")
    create_room_data = {
        "user_id": TEST_USER_ID,
        "title": "Test Chat Room 🚀"
    }
    response = requests.post(f"{BASE_URL}/rooms", json=create_room_data)
    print_response("Tạo phòng chat", response)
    
    if response.status_code == 201:
        room_id = response.json()["id"]
        print(f"\n✅ Room ID: {room_id}")
    else:
        print("\n❌ Không thể tạo phòng chat. Dừng test.")
        return
    
    # 2. Lấy danh sách phòng chat của user
    print("\n\n2️⃣ TEST: Lấy danh sách phòng chat")
    response = requests.get(f"{BASE_URL}/rooms/user/{TEST_USER_ID}?limit=10")
    print_response("Danh sách phòng chat", response)
    
    # 3. Lấy chi tiết phòng chat
    print("\n\n3️⃣ TEST: Lấy chi tiết phòng chat")
    response = requests.get(f"{BASE_URL}/rooms/{room_id}")
    print_response("Chi tiết phòng chat", response)
    
    # 4. Gửi tin nhắn từ user
    print("\n\n4️⃣ TEST: Gửi tin nhắn từ user")
    send_message_data = {
        "chat_room_id": room_id,
        "content": "Hello! Can you help me generate a Python function?",
        "sender_type": "user",
        "metadata": {
            "language": "python",
            "request_type": "code_generation"
        }
    }
    response = requests.post(f"{BASE_URL}/messages", json=send_message_data)
    print_response("Gửi tin nhắn user", response)
    
    if response.status_code == 201:
        message_id = response.json()["id"]
        print(f"\n✅ Message ID: {message_id}")
    else:
        print("\n❌ Không thể gửi tin nhắn")
        message_id = None
    
    # 5. Gửi tin nhắn từ AI (giả lập)
    print("\n\n5️⃣ TEST: Gửi tin nhắn từ AI")
    ai_message_data = {
        "chat_room_id": room_id,
        "content": "Sure! Here's a Python function for you:",
        "sender_type": "ai",
        "metadata": {
            "language": "python",
            "code": "def hello(name):\n    return f'Hello, {name}!'",
            "type": "code_generation"
        }
    }
    response = requests.post(f"{BASE_URL}/messages", json=ai_message_data)
    print_response("Gửi tin nhắn AI", response)
    
    # 6. Lấy tin nhắn trong phòng chat
    print("\n\n6️⃣ TEST: Lấy tin nhắn trong phòng chat")
    response = requests.get(f"{BASE_URL}/messages/room/{room_id}?limit=100")
    print_response("Tin nhắn trong phòng", response)
    
    # 7. Lấy chi tiết một tin nhắn
    if message_id:
        print("\n\n7️⃣ TEST: Lấy chi tiết tin nhắn")
        response = requests.get(f"{BASE_URL}/messages/{message_id}")
        print_response("Chi tiết tin nhắn", response)
    
    # 8. Cập nhật tiêu đề phòng chat
    print("\n\n8️⃣ TEST: Cập nhật tiêu đề phòng chat")
    update_room_data = {
        "title": "Updated Title - Python Help 🐍"
    }
    response = requests.put(f"{BASE_URL}/rooms/{room_id}", json=update_room_data)
    print_response("Cập nhật tiêu đề", response)
    
    # 9. Xóa phòng chat
    print("\n\n9️⃣ TEST: Xóa phòng chat")
    print("⚠️  Bỏ qua bước này để giữ dữ liệu test...")
    # response = requests.delete(f"{BASE_URL}/rooms/{room_id}")
    # print_response("Xóa phòng chat", response)
    
    print("\n\n" + "="*60)
    print("✅ HOÀN THÀNH TEST!")
    print("="*60)
    print(f"\n📝 Room ID để test tiếp: {room_id}")
    print(f"🔗 Xem tất cả endpoints tại: http://localhost:8000/docs")


if __name__ == "__main__":
    try:
        test_chat_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Không thể kết nối đến server!")
        print("📌 Hãy chắc chắn server đang chạy:")
        print("   cd BE")
        print("   python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
