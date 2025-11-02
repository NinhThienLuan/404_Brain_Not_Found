"""
Test script cho Agent Orchestration API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def test_agent_orchestration():
    """Test complete Agent Orchestration workflow"""
    
    print_section("🚀 AGENT ORCHESTRATION API TEST")
    
    # Step 1: Create Session
    print_section("Step 1: Tạo Session")
    
    session_data = {
        "user_id": "test_user_" + str(int(time.time())),
        "metadata": {"source": "test_script"}
    }
    
    response = requests.post(f"{BASE_URL}/agent/session/create", json=session_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        session = response.json()
        session_id = session["session_id"]
        print(f"✅ Session created successfully!")
        print(f"Session ID: {session_id}")
        print(f"User ID: {session['user_id']}")
        print(f"Current Step: {session['current_step']}")
    else:
        print(f"❌ Failed to create session")
        print(response.text)
        return
    
    time.sleep(1)
    
    # Step 2: Parse Context (F1)
    print_section("Step 2: Parse Context (F1)")
    
    context_text = """
    Tôi muốn tạo một API để quản lý sản phẩm trong cửa hàng.
    Cần có các chức năng CRUD: thêm sản phẩm, xem danh sách, cập nhật, và xóa sản phẩm.
    Input: tên sản phẩm, giá, số lượng tồn kho.
    Output: JSON response với thông tin sản phẩm.
    Sử dụng FastAPI và MongoDB.
    """
    
    params = {
        "session_id": session_id,
        "context_text": context_text.strip(),
        "model": "gemini-2.5-flash"
    }
    
    response = requests.post(f"{BASE_URL}/agent/context/parse", params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Context parsed successfully!")
        print(f"Confidence Score: {result.get('confidence_score', 0):.2f}")
        print(f"\nParsed JSON:")
        print(json.dumps(result.get("context_json", {}), indent=2, ensure_ascii=False))
    else:
        print(f"❌ Failed to parse context")
        print(response.text)
    
    time.sleep(2)
    
    # Step 3: Process Prompt (F2) - Generate Code
    print_section("Step 3: Process Prompt (F2) - Generate Code")
    
    prompt_data = {
        "session_id": session_id,
        "user_id": session_data["user_id"],
        "prompt": "Tạo function để thêm sản phẩm mới vào database",
        "model": "gemini-2.5-flash"
    }
    
    response = requests.post(f"{BASE_URL}/agent/prompt/process", json=prompt_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Code generated successfully!")
        print(f"Intent: {result.get('intent', 'N/A')}")
        print(f"Current Step: {result['current_step']}")
        print(f"\nGenerated Code:")
        print("-" * 60)
        print(result.get("generated_code", "No code generated"))
        print("-" * 60)
    else:
        print(f"❌ Failed to generate code")
        print(response.text)
    
    time.sleep(2)
    
    # Step 4: Analyze Code (F3)
    print_section("Step 4: Analyze Code (F3)")
    
    params = {"session_id": session_id}
    response = requests.post(f"{BASE_URL}/agent/code/analyze", params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Code analyzed successfully!")
        print(f"\nAnalysis:")
        print("-" * 60)
        print(result.get("code_analysis", "No analysis available"))
        print("-" * 60)
    else:
        print(f"❌ Failed to analyze code")
        print(response.text)
    
    time.sleep(1)
    
    # Step 5: Get Session Info
    print_section("Step 5: Get Session Info")
    
    response = requests.get(f"{BASE_URL}/agent/session/{session_id}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        session = response.json()
        print(f"✅ Session info retrieved!")
        print(f"User ID: {session['user_id']}")
        print(f"Current Step: {session['current_step']}")
        print(f"Code History Count: {len(session.get('code_history', []))}")
        print(f"\nContext JSON:")
        print(json.dumps(session.get("context_json", {}), indent=2, ensure_ascii=False))
    else:
        print(f"❌ Failed to get session")
        print(response.text)
    
    print_section("🎉 TEST COMPLETED!")
    print(f"Session ID: {session_id}")
    print("Check http://localhost:8000/docs for full API documentation")


if __name__ == "__main__":
    try:
        print("\n🔍 Testing Agent Orchestration API...")
        print(f"Backend URL: {BASE_URL}")
        print("Make sure the backend is running: python -m BE.main\n")
        
        # Test health first
        try:
            health = requests.get(f"{BASE_URL}/health")
            if health.status_code == 200:
                print("✅ Backend is running!\n")
            else:
                print("⚠️ Backend health check failed")
                exit(1)
        except:
            print("❌ Cannot connect to backend!")
            print(f"Please start backend: python -m BE.main")
            exit(1)
        
        # Run tests
        test_agent_orchestration()
        
    except KeyboardInterrupt:
        print("\n\n⏸️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

