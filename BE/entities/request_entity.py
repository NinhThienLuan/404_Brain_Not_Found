"""
Request Entity - Đại diện cho user request
"""
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class Request:
    """
    Request Entity - Domain model cho user requests
    """
    request_type: str  # code_generation, code_review, execution
    user_id: str
    status: str  # pending, processing, completed, failed
    id: Optional[str] = None
    data: Optional[Dict] = None
    result_id: Optional[str] = None  # ID of CodeGeneration/CodeReview/ExecutionLog
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'Request':
        """Tạo Request entity từ dictionary"""
        return Request(
            id=str(data["_id"]) if "_id" in data else None,
            request_type=data["request_type"],
            user_id=data["user_id"],
            status=data["status"],
            data=data.get("data"),
            result_id=data.get("result_id"),
            error_message=data.get("error_message"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển Request entity thành dictionary"""
        result = {
            "request_type": self.request_type,
            "user_id": self.user_id,
            "status": self.status,
            "data": self.data,
            "result_id": self.result_id,
            "error_message": self.error_message,
            "created_at": self.created_at or datetime.utcnow(),
            "updated_at": self.updated_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển Request entity thành response dictionary"""
        return {
            "_id": self.id,
            "request_type": self.request_type,
            "user_id": self.user_id,
            "status": self.status,
            "data": self.data,
            "result_id": self.result_id,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"Request(id={self.id}, type={self.request_type}, status={self.status})"

