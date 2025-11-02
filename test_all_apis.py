"""
Test tất cả API endpoints
Chạy sau khi start server: python -m BE.main
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def test_endpoint(method, url, description, body=None):
    """Test một endpoint"""
    print(f"{YELLOW}Testing: {description}{RESET}")
    print(f"  {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=body)
        else:
            response = requests.delete(url)
        
        if response.status_code < 400:
            print(f"  {GREEN}✓ Status: {response.status_code}{RESET}")
            data = response.json()
            
            # Show relevant info
            if isinstance(data, dict):
                if "total" in data:
                    print(f"  {GREEN}  → Total items: {data['total']}{RESET}")
                elif "items" in data:
                    print(f"  {GREEN}  → Items: {len(data['items'])}{RESET}")
                elif "message" in data:
                    print(f"  {GREEN}  → {data['message']}{RESET}")
            
            return True
        else:
            print(f"  {RED}✗ Status: {response.status_code}{RESET}")
            print(f"  {RED}  Error: {response.text[:100]}{RESET}")
            return False
    except Exception as e:
        print(f"  {RED}✗ Error: {str(e)[:100]}{RESET}")
        return False


def main():
    """Test tất cả APIs"""
    print(f"\n{BLUE}{'='*70}")
    print(f"  🧪 TESTING ALL API ENDPOINTS")
    print(f"{'='*70}{RESET}\n")
    
    results = []
    
    # Test Health Check
    print(f"\n{BLUE}═══ Health Check ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/", "Root endpoint"))
    results.append(test_endpoint("GET", f"{BASE_URL}/health", "Health endpoint"))
    
    # Test Users
    print(f"\n{BLUE}═══ Users API ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/api/users/", "List users"))
    
    # Test Requests
    print(f"\n{BLUE}═══ Requests API ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/api/requests/", "List requests"))
    results.append(test_endpoint("GET", f"{BASE_URL}/api/requests/?language=Python", "Filter by language"))
    
    # Test Code Generations
    print(f"\n{BLUE}═══ Code Generations API ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/api/code-generations/", "List code generations"))
    results.append(test_endpoint("GET", f"{BASE_URL}/api/code-generations/?status=success", "Filter by status"))
    
    # Test Code Reviews
    print(f"\n{BLUE}═══ Code Reviews API ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/api/code-reviews/", "List code reviews"))
    results.append(test_endpoint("GET", f"{BASE_URL}/api/code-reviews/?min_score=7&max_score=10", "Filter by score"))
    
    # Test Execution Logs
    print(f"\n{BLUE}═══ Execution Logs API ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/api/execution-logs/", "List execution logs"))
    
    # Test Chat Rooms
    print(f"\n{BLUE}═══ Chat Rooms API ═══{RESET}")
    results.append(test_endpoint("GET", f"{BASE_URL}/api/chat-rooms/", "List chat rooms"))
    results.append(test_endpoint("GET", f"{BASE_URL}/api/chat-rooms/?active_only=true", "Filter active only"))
    
    # Summary
    print(f"\n{BLUE}{'='*70}")
    print(f"  📊 TEST SUMMARY")
    print(f"{'='*70}{RESET}\n")
    
    passed = sum(results)
    total = len(results)
    
    print(f"  {GREEN if passed == total else YELLOW}Passed: {passed}/{total}{RESET}")
    
    if passed == total:
        print(f"\n  {GREEN}🎉 TẤT CẢ ENDPOINTS ĐỀU HOẠT ĐỘNG!{RESET}\n")
    else:
        print(f"\n  {YELLOW}⚠️  Một số endpoints chưa hoạt động (có thể do collection trống){RESET}\n")
    
    print(f"  {BLUE}Next: Mở http://localhost:8000/docs để test chi tiết hơn{RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}❌ LỖI: Server chưa chạy!{RESET}")
        print(f"{YELLOW}Chạy server trước: python -m BE.main{RESET}\n")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Test bị ngắt{RESET}\n")

