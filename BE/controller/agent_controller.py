"""
Agent Controller - API endpoints cho Agent Orchestration
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from BE.model.orchestration_models import (
    AgentRequest,
    AgentResponse,
    SessionCreateRequest,
    SessionResponse,
    ContextParseRequest,
    ContextParseResponse
)
from BE.service.agent_orchestration_service import AgentOrchestrationService


# Create router
agent_router = APIRouter(prefix="/agent", tags=["Agent Orchestration"])

# Initialize service
agent_service = AgentOrchestrationService()


# ==================== SESSION ENDPOINTS ====================

@agent_router.post(
    "/session/create",
    response_model=SessionResponse,
    summary="Create New Session",
    description="Tạo session mới cho user để bắt đầu làm việc"
)
async def create_session(request: SessionCreateRequest) -> SessionResponse:
    """Tạo session mới"""
    try:
        return agent_service.create_session(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@agent_router.get(
    "/session/{session_id}",
    response_model=SessionResponse,
    summary="Get Session Info",
    description="Lấy thông tin session hiện tại"
)
async def get_session(session_id: str) -> SessionResponse:
    """Lấy thông tin session"""
    session = agent_service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


# ==================== FLOW 1: CONTEXT PARSING ====================

@agent_router.post(
    "/context/parse",
    response_model=AgentResponse,
    summary="Parse Context (F1)",
    description="Luồng F1: Parse context text thành JSON structure"
)
async def parse_context(
    session_id: str,
    context_text: str,
    model: str = "gemini-2.5-flash"
) -> AgentResponse:
    """
    Parse context từ user
    
    - **session_id**: ID của session
    - **context_text**: Text mô tả context/yêu cầu từ user
    - **model**: Model để sử dụng
    """
    try:
        return agent_service.process_context(session_id, context_text, model)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== FLOW 2: PROMPT PROCESSING ====================

@agent_router.post(
    "/prompt/process",
    response_model=AgentResponse,
    summary="Process Prompt (F2)",
    description="Luồng F2: Classify intent và generate code"
)
async def process_prompt(request: AgentRequest) -> AgentResponse:
    """
    Process prompt từ user
    
    Workflow:
    1. Classify intent (create_new / modify_existing / analyze)
    2. Generate code dựa trên intent
    3. Save vào history
    """
    try:
        return agent_service.process_prompt(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== FLOW 3: CODE ANALYSIS ====================

@agent_router.post(
    "/code/analyze",
    response_model=AgentResponse,
    summary="Analyze Code (F3)",
    description="Luồng F3: Phân tích code và tạo summary"
)
async def analyze_code(session_id: str) -> AgentResponse:
    """
    Analyze code vừa generate
    
    - **session_id**: ID của session
    """
    try:
        return agent_service.analyze_code(session_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@agent_router.get(
    "/health",
    summary="Health Check",
    description="Check if Agent Orchestration service is running"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Agent Orchestration API",
        "version": "1.0.0",
        "features": [
            "Session Management",
            "Context Parsing (F1)",
            "Prompt Processing (F2)",
            "Code Analysis (F3)"
        ]
    }

