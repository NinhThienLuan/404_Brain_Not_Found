"""
Test Intent Classifier Service
"""
import sys
import os

# Add BE directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.intent_classifier_service import IntentClassifierService
from model.intent_models import IntentClassifierRequest, IntentType


def test_new_request_generate_code():
    """Test luồng B: Yêu cầu mới -> Generate Code"""
    print("=== Test 1: New Request -> Generate Code ===")

    service = IntentClassifierService()
    request = IntentClassifierRequest(
        user_message="Tạo hàm tính tổng hai số",
        session_id="session_1"
    )

    result = service.classify_intent(request)

    print(f"Intent: {result.intent}")
    print(f"Data: {result.data}")
    print(f"Session ID: {result.session_id}")

    assert result.intent == IntentType.GENERATE_CODE
    assert "completed_json" in result.data
    print("✅ PASSED\n")


def test_new_request_modify_code():
    """Test luồng B: Yêu cầu mới -> Modify Code"""
    print("=== Test 2: New Request -> Modify Code ===")

    service = IntentClassifierService()
    request = IntentClassifierRequest(
        user_message="Sửa lỗi hàm calculate_sum",
        session_id="session_2"
    )

    result = service.classify_intent(request)

    print(f"Intent: {result.intent}")
    print(f"Data: {result.data}")

    assert result.intent == IntentType.MODIFY_CODE
    assert result.data["user_message"] == "Sửa lỗi hàm calculate_sum"
    print("✅ PASSED\n")


def test_new_request_chitchat():
    """Test luồng B: Yêu cầu mới -> Chitchat"""
    print("=== Test 3: New Request -> Chitchat ===")

    service = IntentClassifierService()
    request = IntentClassifierRequest(
        user_message="Chào bạn",
        session_id="session_3"
    )

    result = service.classify_intent(request)

    print(f"Intent: {result.intent}")
    print(f"Response: {result.response_message}")

    assert result.intent == IntentType.CHITCHAT
    assert "Chào bạn" in result.response_message
    print("✅ PASSED\n")


def main():
    """Run all tests"""
    print("🚀 INTENT CLASSIFIER SERVICE - TESTS\n")

    try:
        test_new_request_generate_code()
        test_new_request_modify_code()
        test_new_request_chitchat()

        print("🎉 ALL TESTS PASSED!")

    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()