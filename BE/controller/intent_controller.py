"""
Intent Controller - API cho Intent Classifier Service
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from BE.service.intent_classifier_service import IntentClassifierService
from BE.model.intent_models import IntentClassifierRequest, IntentClassifierResponse


# Create router
router = APIRouter(prefix="/intent", tags=["Intent Classifier"])

# Initialize service
intent_service = IntentClassifierService()


@router.post("/classify", response_model=IntentClassifierResponse)
async def classify_intent(request: IntentClassifierRequest) -> IntentClassifierResponse:
    """
    Phân loại intent từ user message

    - **user_message**: Tin nhắn từ người dùng
    - **session_id**: ID phiên để lưu trữ state
    """
    try:
        result = intent_service.classify_intent(request)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi phân loại intent: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    from BE.model.intent_models import IntentType
    return {
        "status": "healthy",
        "service": "Intent Classifier Service",
        "supported_intents": [intent.value for intent in IntentType]
    }