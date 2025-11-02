"""
Comprehensive integration-style tests for main features.
Mocks Gemini interactions and SessionRepository (no network / DB required).

Run from repo root with PYTHONPATH set, e.g.:

$env:PYTHONPATH='D:\Semester5\HACKATHON\404_Brain_Not_Found'
python BE/test_all_features.py

"""
import sys
import os
from datetime import datetime

# Ensure repo root is on path when running tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BE.service.context_parsing_service import ContextParsingService
from BE.service.ai_service import CodeGenerationService
from BE.service.agent_orchestration_service import AgentOrchestrationService
from BE.entities.session_entity import Session, WorkflowStep
from BE.model.ai_models import CodeGenerationRequest


# --- Fake Gemini repository ---
class FakeGeminiRepo:
    def __init__(self):
        pass

    def generate_code(self, prompt: str, model_name: str = "gemini-2.5-flash") -> str:
        # If prompt looks like extraction prompt, return JSON expected by ContextParsingService
        if 'CONTEXT DAU VAO' in prompt or prompt.strip().startswith('Ban la mot Ky su'):
            # Minimal valid JSON for parsing
            return '{"function_name": "factorial", "purpose": "Tính giai thừa", "inputs": [{"name": "n", "type": "int", "description": "số nguyên không âm"}], "core_logic": ["kiểm tra n <=1", "lặp để nhân các số"], "outputs": {"type": "int", "description": "giai thừa của n"}}'

        # Otherwise respond with a code block
        return '```python\ndef factorial(n: int) -> int:\n    """Compute factorial"""\n    if n <= 1:\n        return 1\n    result = 1\n    for i in range(2, n+1):\n        result *= i\n    return result\n```'

    def review_code(self, code: str, language: str, review_type: str = "general", model_name: str = "gemini-2.5-flash") -> str:
        return "Overall score: 8. Suggestions: none."


# --- Fake Session Repository (in-memory) ---
class FakeSessionRepository:
    def __init__(self):
        self.store = {}
        self._id_counter = 1

    def create(self, session: Session) -> Session:
        sid = f"fake_{self._id_counter}"
        self._id_counter += 1
        session.id = sid
        session.created_at = session.created_at or datetime.utcnow()
        session.updated_at = session.updated_at or datetime.utcnow()
        self.store[sid] = session
        return session

    def find_by_id(self, session_id: str):
        return self.store.get(session_id)

    def update(self, session: Session):
        if not session.id:
            return None
        session.updated_at = datetime.utcnow()
        self.store[session.id] = session
        return session

    def update_step(self, session_id: str, new_step: WorkflowStep) -> bool:
        s = self.store.get(session_id)
        if not s:
            return False
        s.current_step = new_step
        s.updated_at = datetime.utcnow()
        self.store[session_id] = s
        return True

    def add_code_history(self, session_id: str, code_entry: dict) -> bool:
        s = self.store.get(session_id)
        if not s:
            return False
        s.code_history.append(code_entry)
        s.updated_at = datetime.utcnow()
        return True


# --- Tests ---

def test_context_parsing():
    fake = FakeGeminiRepo()
    cps = ContextParsingService(gemini_repo=fake)

    user_context = "Tạo một hàm tính giai thừa nhận n"
    ok, parsed, err = cps.extract_one_shot(user_context)
    assert ok, f"Parsing failed: {err}"
    details = parsed.details
    assert details.get("function_name") == "factorial"
    assert details.get("purpose") == "Tính giai thừa"
    print("test_context_parsing: PASSED")


def test_code_generation_service():
    fake = FakeGeminiRepo()
    svc = CodeGenerationService(gemini_repo=fake)

    req = CodeGenerationRequest(
        prompt="Tạo hàm tính giai thừa",
        language="python",
        additional_context=None,
        model="gemini-2.5-flash"
    )

    resp = svc.generate_code(req)
    assert resp.success, f"Code gen failed: {resp.error_message}"
    assert "def factorial" in resp.generated_code
    print("test_code_generation_service: PASSED")


def test_orchestration_flow():
    # Setup agent with fakes
    fake_gem = FakeGeminiRepo()
    agent = AgentOrchestrationService()

    # Replace repositories/services with fakes to avoid DB and external calls
    agent.session_repo = FakeSessionRepository()
    agent.context_parsing_service = ContextParsingService(gemini_repo=fake_gem)
    agent.code_gen_service = CodeGenerationService(gemini_repo=fake_gem)

    # Create a session
    session = Session(user_id="user_test")
    saved = agent.session_repo.create(session)

    # Run process_context which should parse and then generate code
    resp = agent.process_context(saved.id, "Tạo hàm tính giai thừa", model="gemini-2.5-flash")
    assert resp.success, f"Orchestration failed: {resp.message} {resp.error_message}"
    assert resp.generated_code is not None
    print("test_orchestration_flow: PASSED")


if __name__ == "__main__":
    test_context_parsing()
    test_code_generation_service()
    test_orchestration_flow()
    print("ALL TESTS PASSED")
