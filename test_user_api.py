"""
Script test User API
Chạy script này sau khi đã start server (python -m BE.main)
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    """In tiêu đề section"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_response(response):
    """In response đẹp"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

# Test health check
print_section("1. Health Check")
response = requests.get(f"{BASE_URL}/")
print_response(response)

# Test tạo user mới
print_section("2. Tạo User Mới")
response = requests.post(f"{BASE_URL}/api/users/", json={
    "name": "Phạm Văn Test",
    "email": "test@example.com"
})
print_response(response)

if response.status_code == 201:
    user = response.json()
    user_id = user["_id"]
    
    # Test get user by ID
    print_section("3. Lấy User Theo ID")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")
    print_response(response)
    
    # Test get user by email
    print_section("4. Lấy User Theo Email")
    response = requests.get(f"{BASE_URL}/api/users/email/test@example.com")
    print_response(response)
    
    # Test update user
    print_section("5. Update User")
    response = requests.put(f"{BASE_URL}/api/users/{user_id}", json={
        "name": "Phạm Văn Test Updated"
    })
    print_response(response)
    
    # Test get all users
    print_section("6. Lấy Danh Sách Users")
    response = requests.get(f"{BASE_URL}/api/users/?page=1&page_size=10")
    print_response(response)
    
    # Test delete user
    print_section("7. Xóa User")
    response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    print_response(response)
    
    # Verify deleted
    print_section("8. Verify User Đã Bị Xóa")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")
    print_response(response)

# Test error cases
print_section("9. Test Error - Email Trùng")
requests.post(f"{BASE_URL}/api/users/", json={
    "name": "User 1",
    "email": "duplicate@example.com"
})
response = requests.post(f"{BASE_URL}/api/users/", json={
    "name": "User 2",
    "email": "duplicate@example.com"
})
print_response(response)

print_section("10. Test Error - User Không Tồn Tại")
response = requests.get(f"{BASE_URL}/api/users/invalid_id_123")
print_response(response)

print("\n✅ Test hoàn tất!")

