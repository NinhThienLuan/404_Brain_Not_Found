"""
Session Entity - Quản lý phiên làm việc của user
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from bson import ObjectId
from enum import Enum


class WorkflowStep(str, Enum):
    """Các bước trong workflow"""
    IDLE = "idle"
    PARSING_CONTEXT = "parsing_context"
    CLASSIFYING_INTENT = "classifying_intent"
    GENERATING_CODE = "generating_code"
    ANALYZING_CODE = "analyzing_code"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class Session:
    """
    Session Entity - Đại diện cho một phiên làm việc
    
    Lưu trữ:
    - State hiện tại (đang ở bước nào)
    - Context đã được parse
    - Lịch sử code đã generate
    - Metadata khác
    """
    user_id: str
    current_step: WorkflowStep = WorkflowStep.IDLE
    context_json: Optional[Dict[str, Any]] = None
    code_history: List[Dict[str, Any]] = field(default_factory=list)
    last_intent: Optional[str] = None
    last_prompt: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'Session':
        """Tạo Session từ MongoDB document"""
        return Session(
            id=str(data["_id"]) if "_id" in data else None,
            user_id=data["user_id"],
            current_step=WorkflowStep(data.get("current_step", "idle")),
            context_json=data.get("context_json"),
            code_history=data.get("code_history", []),
            last_intent=data.get("last_intent"),
            last_prompt=data.get("last_prompt"),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển Session thành dictionary để lưu vào MongoDB"""
        now = datetime.utcnow()
        
        # Ensure datetime objects are set
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
        
        result = {
            "user_id": self.user_id,
            "current_step": self.current_step.value,
            "context_json": self.context_json,
            "code_history": self.code_history,
            "last_intent": self.last_intent,
            "last_prompt": self.last_prompt,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển thành response cho API"""
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "current_step": self.current_step.value,
            "context_json": self.context_json,
            "code_history": self.code_history,
            "last_intent": self.last_intent,
            "last_prompt": self.last_prompt,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def add_code_to_history(self, code: str, language: str, description: str = ""):
        """Thêm code vào lịch sử"""
        self.code_history.append({
            "code": code,
            "language": language,
            "description": description,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def update_step(self, new_step: WorkflowStep):
        """Cập nhật bước hiện tại"""
        self.current_step = new_step
        self.updated_at = datetime.utcnow()

