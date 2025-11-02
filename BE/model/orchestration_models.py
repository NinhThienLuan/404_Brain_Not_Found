"""
Pydantic models cho Agent Orchestration
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class IntentType(str, Enum):
    """Loại intent của user"""
    CREATE_NEW = "create_new"
    MODIFY_EXISTING = "modify_existing"
    ANALYZE = "analyze"
    UNKNOWN = "unknown"


# ==================== CONTEXT PARSING ====================

class ContextParseRequest(BaseModel):
    """Request để parse context"""
    session_id: str = Field(..., description="ID của session")
    context_text: str = Field(..., description="Raw text context từ user")
    model: str = Field(default="gemini-2.5-flash", description="Model để sử dụng")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "session_123",
                "context_text": "Tạo một API để quản lý sản phẩm với CRUD operations, input là product name và price, output là JSON",
                "model": "gemini-2.5-flash"
            }
        }
    }


class ContextParseResponse(BaseModel):
    """Response sau khi parse context"""
    session_id: str
    parsed_json: Dict[str, Any]
    confidence_score: float
    success: bool
    error_message: Optional[str] = None
    timestamp: datetime


# ==================== AGENT ORCHESTRATION ====================

class AgentRequest(BaseModel):
    """Request chung cho agent orchestration"""
    session_id: str = Field(..., description="ID của session")
    user_id: str = Field(..., description="ID của user")
    prompt: str = Field(..., description="Prompt từ user")
    model: str = Field(default="gemini-2.5-flash", description="Model để sử dụng")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "session_123",
                "user_id": "user_456",
                "prompt": "Tạo function để tính tổng hai số",
                "model": "gemini-2.5-flash"
            }
        }
    }


class AgentResponse(BaseModel):
    """Response từ agent orchestration"""
    session_id: str
    current_step: str
    intent: Optional[str] = None
    generated_code: Optional[str] = None
    code_analysis: Optional[str] = None
    context_json: Optional[Dict[str, Any]] = None
    success: bool
    message: str
    timestamp: datetime
    error_message: Optional[str] = None


class SessionCreateRequest(BaseModel):
    """Request để tạo session mới"""
    user_id: str = Field(..., description="ID của user")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata tùy chọn")


class SessionResponse(BaseModel):
    """Response chứa thông tin session"""
    session_id: str
    user_id: str
    current_step: str
    context_json: Optional[Dict[str, Any]] = None
    code_history: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: datetime


class IntentClassifyRequest(BaseModel):
    """Request để classify intent"""
    prompt: str = Field(..., description="Prompt từ user")
    context_json: Optional[Dict[str, Any]] = Field(default=None, description="Context hiện tại")


class IntentClassifyResponse(BaseModel):
    """Response sau khi classify intent"""
    intent: IntentType
    confidence: float
    reasoning: str
    success: bool

