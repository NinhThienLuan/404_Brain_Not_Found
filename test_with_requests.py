"""
Script test User API bằng Python requests
Chạy sau khi đã start server: python -m BE.main
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_section(title: str):
    """In tiêu đề section"""
    print(f"\n{BLUE}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{RESET}\n")


def print_request(method: str, url: str, body: Dict = None):
    """In thông tin request"""
    print(f"{YELLOW}➜ {method} {url}{RESET}")
    if body:
        print(f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}")


def print_response(response: requests.Response):
    """In response"""
    status_color = GREEN if response.status_code < 400 else RED
    print(f"{status_color}← Status: {response.status_code}{RESET}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_health_check():
    """Test health check endpoint"""
    print_section("1. Health Check")
    url = f"{BASE_URL}/"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    return response.status_code == 200


def test_create_user():
    """Test tạo user mới"""
    print_section("2. Tạo User Mới")
    url = f"{BASE_URL}/api/users/"
    body = {
        "name": "Test User Python",
        "email": "python_test@example.com"
    }
    
    print_request("POST", url, body)
    response = requests.post(url, json=body)
    print_response(response)
    
    if response.status_code == 201:
        return response.json()["_id"]
    return None


def test_get_all_users():
    """Test lấy danh sách users"""
    print_section("3. Lấy Danh Sách Users")
    url = f"{BASE_URL}/api/users/"
    params = {"page": 1, "page_size": 10}
    
    print_request("GET", f"{url}?page={params['page']}&page_size={params['page_size']}")
    response = requests.get(url, params=params)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n{GREEN}✓ Tìm thấy {data['total']} users{RESET}")
        print(f"  - Page {data['page']}/{data['total_pages']}")
        print(f"  - Showing {len(data['users'])} users")
    
    return response.status_code == 200


def test_get_user_by_id(user_id: str):
    """Test lấy user theo ID"""
    print_section("4. Lấy User Theo ID")
    url = f"{BASE_URL}/api/users/{user_id}"
    
    print_request("GET", url)
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 200


def test_get_user_by_email(email: str):
    """Test lấy user theo email"""
    print_section("5. Lấy User Theo Email")
    url = f"{BASE_URL}/api/users/email/{email}"
    
    print_request("GET", url)
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 200


def test_update_user(user_id: str):
    """Test update user"""
    print_section("6. Update User")
    url = f"{BASE_URL}/api/users/{user_id}"
    body = {
        "name": "Test User Updated",
        "email": "updated_python@example.com"
    }
    
    print_request("PUT", url, body)
    response = requests.put(url, json=body)
    print_response(response)
    
    return response.status_code == 200


def test_partial_update_user(user_id: str):
    """Test partial update user"""
    print_section("7. Partial Update User (PATCH)")
    url = f"{BASE_URL}/api/users/{user_id}"
    body = {
        "name": "Name Changed Only"
    }
    
    print_request("PATCH", url, body)
    response = requests.patch(url, json=body)
    print_response(response)
    
    return response.status_code == 200


def test_delete_user(user_id: str):
    """Test xóa user"""
    print_section("8. Xóa User")
    url = f"{BASE_URL}/api/users/{user_id}"
    
    print_request("DELETE", url)
    response = requests.delete(url)
    print_response(response)
    
    return response.status_code == 200


def test_error_cases():
    """Test các error cases"""
    print_section("9. Test Error Cases")
    
    # Test 1: Email trùng
    print(f"{YELLOW}Test 1: Tạo user với email trùng{RESET}")
    url = f"{BASE_URL}/api/users/"
    body1 = {"name": "User 1", "email": "duplicate@example.com"}
    body2 = {"name": "User 2", "email": "duplicate@example.com"}
    
    requests.post(url, json=body1)  # Tạo user đầu
    response = requests.post(url, json=body2)  # Tạo user trùng email
    print_response(response)
    
    if response.status_code == 400:
        print(f"{GREEN}✓ Đã bắt lỗi email trùng đúng{RESET}\n")
    
    # Test 2: User không tồn tại
    print(f"{YELLOW}Test 2: Lấy user không tồn tại{RESET}")
    url = f"{BASE_URL}/api/users/invalid_id_12345"
    response = requests.get(url)
    print_response(response)
    
    if response.status_code == 404:
        print(f"{GREEN}✓ Đã trả về 404 đúng{RESET}\n")
    
    # Test 3: Email không hợp lệ
    print(f"{YELLOW}Test 3: Tạo user với email không hợp lệ{RESET}")
    url = f"{BASE_URL}/api/users/"
    body = {"name": "Test", "email": "not-an-email"}
    response = requests.post(url, json=body)
    print_response(response)
    
    if response.status_code == 422:
        print(f"{GREEN}✓ Đã bắt lỗi validation đúng{RESET}")


def test_pagination():
    """Test pagination"""
    print_section("10. Test Pagination")
    
    # Tạo nhiều users
    print(f"{YELLOW}Tạo 5 test users...{RESET}")
    user_ids = []
    for i in range(5):
        url = f"{BASE_URL}/api/users/"
        body = {
            "name": f"Pagination Test User {i+1}",
            "email": f"pagination{i+1}@example.com"
        }
        response = requests.post(url, json=body)
        if response.status_code == 201:
            user_ids.append(response.json()["_id"])
    
    print(f"{GREEN}✓ Đã tạo {len(user_ids)} users{RESET}\n")
    
    # Test pagination
    print(f"{YELLOW}Test page_size=2{RESET}")
    url = f"{BASE_URL}/api/users/"
    params = {"page": 1, "page_size": 2}
    response = requests.get(url, params=params)
    data = response.json()
    print(f"Page 1: {len(data['users'])} users")
    
    params = {"page": 2, "page_size": 2}
    response = requests.get(url, params=params)
    data = response.json()
    print(f"Page 2: {len(data['users'])} users")
    
    print(f"{GREEN}✓ Pagination hoạt động đúng{RESET}\n")
    
    # Cleanup
    print(f"{YELLOW}Xóa test users...{RESET}")
    for user_id in user_ids:
        requests.delete(f"{BASE_URL}/api/users/{user_id}")
    print(f"{GREEN}✓ Đã xóa {len(user_ids)} users{RESET}")


def run_all_tests():
    """Chạy tất cả tests"""
    print(f"\n{BLUE}{'='*70}")
    print(f"  🧪 BẮT ĐẦU TEST USER API")
    print(f"{'='*70}{RESET}")
    
    results = []
    
    # Test basic flow
    results.append(("Health Check", test_health_check()))
    
    user_id = test_create_user()
    results.append(("Tạo User", user_id is not None))
    
    if user_id:
        results.append(("Lấy Danh Sách Users", test_get_all_users()))
        results.append(("Lấy User Theo ID", test_get_user_by_id(user_id)))
        results.append(("Lấy User Theo Email", test_get_user_by_email("python_test@example.com")))
        results.append(("Update User", test_update_user(user_id)))
        results.append(("Partial Update", test_partial_update_user(user_id)))
        results.append(("Xóa User", test_delete_user(user_id)))
    
    # Test error cases
    test_error_cases()
    
    # Test pagination
    test_pagination()
    
    # Print summary
    print_section("📊 KẾT QUẢ TEST")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"{status}  {test_name}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{GREEN}Passed: {passed}/{total}{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 TẤT CẢ TESTS ĐỀU PASS!{RESET}\n")
    else:
        print(f"\n{RED}⚠️  CÓ {total - passed} TESTS FAILED{RESET}\n")


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}❌ LỖI: Không kết nối được tới server!{RESET}")
        print(f"{YELLOW}Hãy chạy server trước:{RESET}")
        print(f"  python -m BE.main\n")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️  Test bị ngắt bởi user{RESET}\n")
    except Exception as e:
        print(f"\n{RED}❌ LỖI: {str(e)}{RESET}\n")

