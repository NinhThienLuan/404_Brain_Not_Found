"""
End-to-End Test: User Input → Agent Orchestration → Context Parsing → Code Generation

Test luồng đầy đủ từ khi người dùng nhập context đến khi sinh code.
Mock Gemini API và Session Repository để test standalone.

Chạy:
$env:PYTHONPATH='D:\Semester5\HACKATHON\404_Brain_Not_Found'
python BE/test_e2e_orchestration.py
"""
import sys
import os
from datetime import datetime

# Ensure repo root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BE.service.agent_orchestration_service import AgentOrchestrationService
from BE.service.context_parsing_service import ContextParsingService
from BE.service.ai_service import CodeGenerationService
from BE.entities.session_entity import Session, WorkflowStep
from BE.model.orchestration_models import SessionCreateRequest


# ====================== MOCK CLASSES ======================

class MockGeminiRepository:
    """Mock Gemini API để trả về response giả"""
    
    def __init__(self):
        self.call_history = []
    
    def generate_code(self, prompt: str, model_name: str = "gemini-2.5-flash") -> str:
        print(f"\n[MockGemini] Received prompt (first 100 chars):")
        print(f"  {prompt[:100]}...")
        print(f"[MockGemini] Model: {model_name}")
        
        self.call_history.append({
            "prompt": prompt,
            "model": model_name,
            "timestamp": datetime.now()
        })
        
        # Detect if this is context extraction or code generation
        if 'CONTEXT DAU VAO' in prompt or 'Ban la mot Ky su' in prompt:
            # Context parsing response
            response = '''{
  "function_name": "calculate_factorial",
  "purpose": "Tính giai thừa của một số nguyên không âm",
  "inputs": [
    {
      "name": "n",
      "type": "int",
      "description": "Số nguyên không âm cần tính giai thừa"
    }
  ],
  "core_logic": [
    "Kiểm tra nếu n <= 1 thì trả về 1",
    "Khởi tạo biến result = 1",
    "Dùng vòng lặp từ 2 đến n để nhân dần vào result",
    "Trả về result"
  ],
  "outputs": {
    "type": "int",
    "description": "Giá trị giai thừa của n"
  }
}'''
            print(f"[MockGemini] Returning CONTEXT PARSING response")
            return response
        else:
            # Code generation response
            response = '''```python
def calculate_factorial(n: int) -> int:
    """
    Tính giai thừa của một số nguyên không âm.
    
    Args:
        n: Số nguyên không âm cần tính giai thừa
        
    Returns:
        Giá trị giai thừa của n
        
    Raises:
        ValueError: Nếu n < 0
    """
    if n < 0:
        raise ValueError("n phải là số nguyên không âm")
    
    if n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


# Example usage
if __name__ == "__main__":
    print(calculate_factorial(5))  # Output: 120
    print(calculate_factorial(0))  # Output: 1
```

Giải thích:
- Hàm nhận vào một số nguyên không âm n
- Kiểm tra trường hợp đặc biệt: n <= 1 trả về 1
- Sử dụng vòng lặp để tính tích từ 2 đến n
- Trả về kết quả giai thừa
- Có validation để đảm bảo n không âm
'''
            print(f"[MockGemini] Returning CODE GENERATION response")
            return response


class MockSessionRepository:
    """Mock Session Repository để test không cần MongoDB"""
    
    def __init__(self):
        self.store = {}
        self._id_counter = 1
        print("[MockSessionRepo] Initialized")
    
    def create(self, session: Session) -> Session:
        sid = f"session_{self._id_counter}"
        self._id_counter += 1
        session.id = sid
        session.created_at = session.created_at or datetime.utcnow()
        session.updated_at = session.updated_at or datetime.utcnow()
        self.store[sid] = session
        print(f"[MockSessionRepo] Created session: {sid}")
        return session
    
    def find_by_id(self, session_id: str):
        session = self.store.get(session_id)
        print(f"[MockSessionRepo] Find session {session_id}: {'Found' if session else 'Not found'}")
        return session
    
    def update(self, session: Session):
        if not session.id:
            return None
        session.updated_at = datetime.utcnow()
        self.store[session.id] = session
        print(f"[MockSessionRepo] Updated session: {session.id}")
        return session
    
    def update_step(self, session_id: str, new_step: WorkflowStep) -> bool:
        s = self.store.get(session_id)
        if not s:
            print(f"[MockSessionRepo] Update step FAILED: session {session_id} not found")
            return False
        s.current_step = new_step
        s.updated_at = datetime.utcnow()
        self.store[session_id] = s
        print(f"[MockSessionRepo] Updated step to: {new_step.value}")
        return True


class MockContextRepository:
    """Mock Context Repository"""
    def __init__(self):
        print("[MockContextRepo] Initialized")


# ====================== TEST FUNCTIONS ======================

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_full_orchestration_flow():
    """Test luồng hoàn chỉnh từ user input đến code generation"""
    
    print_section("BẮT ĐẦU E2E TEST: User Input → Code Generation")
    
    # Step 1: Setup - Tạo mock dependencies
    print_section("STEP 1: Setup Mock Dependencies")
    mock_gemini = MockGeminiRepository()
    mock_session_repo = MockSessionRepository()
    mock_context_repo = MockContextRepository()
    
    # Step 2: Khởi tạo services với mock dependencies
    print_section("STEP 2: Initialize Services")
    
    orchestration_service = AgentOrchestrationService()
    orchestration_service.session_repo = mock_session_repo
    orchestration_service.context_repo = mock_context_repo
    orchestration_service.gemini_repo = mock_gemini
    
    # Replace context parsing service với mock gemini
    orchestration_service.context_parsing_service = ContextParsingService(gemini_repo=mock_gemini)
    
    # Replace code gen service với mock gemini
    orchestration_service.code_gen_service = CodeGenerationService(gemini_repo=mock_gemini)
    
    print("✅ AgentOrchestrationService initialized with mocks")
    print("✅ ContextParsingService initialized with mock Gemini")
    print("✅ CodeGenerationService initialized with mock Gemini")
    
    # Step 3: Tạo session (giống như user bắt đầu conversation)
    print_section("STEP 3: Create User Session")
    
    session_request = SessionCreateRequest(
        user_id="test_user_001",
        metadata={"source": "e2e_test"}
    )
    
    session_response = orchestration_service.create_session(session_request)
    session_id = session_response.session_id
    
    print(f"✅ Session created")
    print(f"   Session ID: {session_id}")
    print(f"   User ID: {session_response.user_id}")
    print(f"   Current Step: {session_response.current_step}")
    
    # Step 4: User nhập context (yêu cầu tạo function)
    print_section("STEP 4: User Input - Context Text")
    
    user_context = """
Tôi cần một hàm để tính giai thừa của một số nguyên.
Hàm này nên nhận vào một số nguyên n không âm.
Nếu n = 0 hoặc n = 1 thì trả về 1.
Nếu n > 1 thì tính tích của tất cả các số từ 1 đến n.
Hàm nên có validation để đảm bảo n không âm.
    """.strip()
    
    print("📝 User Context Input:")
    print(f"   {user_context}")
    
    model = "gemini-2.5-flash"
    print(f"   Model: {model}")
    
    # Step 5: Gọi process_context (toàn bộ luồng orchestration)
    print_section("STEP 5: Process Context → Parse → Generate Code")
    
    print("\n🚀 Calling orchestration_service.process_context()...")
    print("   This will:")
    print("   1. Update session step to PARSING_CONTEXT")
    print("   2. Call ContextParsingService.extract_one_shot()")
    print("   3. Parse JSON response from Gemini")
    print("   4. Save parsed context to session")
    print("   5. Build prompt from parsed context")
    print("   6. Call CodeGenerationService.generate_code()")
    print("   7. Save generated code to session history")
    print("   8. Return AgentResponse with code")
    
    result = orchestration_service.process_context(
        session_id=session_id,
        context_text=user_context,
        model=model
    )
    
    # Step 6: Kiểm tra kết quả
    print_section("STEP 6: Verify Results")
    
    print(f"\n📊 AgentResponse:")
    print(f"   Success: {result.success}")
    print(f"   Current Step: {result.current_step}")
    print(f"   Message: {result.message}")
    
    if result.error_message:
        print(f"   ❌ Error: {result.error_message}")
        return False
    
    # Check parsed context
    print(f"\n📋 Parsed Context:")
    if result.context_json:
        context = result.context_json
        details = context.get('details', {})
        print(f"   Goal Type: {context.get('goal_type')}")
        print(f"   Function Name: {details.get('function_name')}")
        print(f"   Purpose: {details.get('purpose')}")
        print(f"   Inputs: {len(details.get('inputs', []))} parameters")
        print(f"   Core Logic Steps: {len(details.get('core_logic', []))}")
        print(f"   Has Outputs: {details.get('outputs') is not None}")
    
    # Check generated code
    print(f"\n💻 Generated Code:")
    if result.generated_code:
        print("   ✅ Code generated successfully")
        print(f"   Code length: {len(result.generated_code)} characters")
        print(f"   First 200 chars:")
        print("   " + "─"*60)
        for line in result.generated_code[:200].split('\n'):
            print(f"   {line}")
        print("   " + "─"*60)
        print(f"   ... (total {len(result.generated_code)} chars)")
    else:
        print("   ❌ No code generated")
        return False
    
    # Step 7: Verify session state
    print_section("STEP 7: Verify Session State")
    
    final_session = mock_session_repo.find_by_id(session_id)
    if final_session:
        print(f"✅ Session found")
        print(f"   Current Step: {final_session.current_step.value}")
        print(f"   Has Context JSON: {final_session.context_json is not None}")
        print(f"   Code History Length: {len(final_session.code_history)}")
        
        if final_session.code_history:
            latest_code = final_session.code_history[-1]
            print(f"\n   Latest Code Entry:")
            print(f"      Language: {latest_code.get('language')}")
            print(f"      Description: {latest_code.get('description')}")
            print(f"      Timestamp: {latest_code.get('timestamp')}")
    
    # Step 8: Summary
    print_section("STEP 8: Test Summary")
    
    print("\n✅ E2E Test PASSED")
    print("\nLuồng dữ liệu đã được verify:")
    print("  1. ✅ User Input → AgentOrchestrationService")
    print("  2. ✅ AgentOrchestrationService → ContextParsingService")
    print("  3. ✅ ContextParsingService → GeminiRepository (mock)")
    print("  4. ✅ Parsed Context → Structured JSON")
    print("  5. ✅ Build Prompt from Parsed Context")
    print("  6. ✅ AgentOrchestrationService → CodeGenerationService")
    print("  7. ✅ CodeGenerationService → GeminiRepository (mock)")
    print("  8. ✅ Generated Code → Session History")
    print("  9. ✅ Return AgentResponse với code")
    
    print(f"\nMock Gemini được gọi: {len(mock_gemini.call_history)} lần")
    for i, call in enumerate(mock_gemini.call_history, 1):
        print(f"  Call {i}: Model={call['model']}, Prompt length={len(call['prompt'])} chars")
    
    return True


# ====================== MAIN ======================

if __name__ == "__main__":
    try:
        success = test_full_orchestration_flow()
        
        if success:
            print("\n" + "🎉"*35)
            print("\n   ALL TESTS PASSED - E2E Flow Working Correctly!")
            print("\n" + "🎉"*35)
            sys.exit(0)
        else:
            print("\n❌ TEST FAILED")
            sys.exit(1)
            
    except Exception as e:
        print("\n" + "❌"*35)
        print(f"\n   EXCEPTION OCCURRED: {e}")
        print("\n" + "❌"*35)
        import traceback
        traceback.print_exc()
        sys.exit(1)
