"""
Request Entity - Đại diện cho user request
Khớp với structure thực tế trong MongoDB
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class Request:
    """
    Request Entity - Domain model cho user requests
    """
    user_id: str
    requirement_text: str
    language: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'Request':
        """Tạo Request entity từ dictionary"""
        return Request(
            id=str(data["_id"]) if "_id" in data else None,
            user_id=str(data["user_id"]) if isinstance(data.get("user_id"), ObjectId) else data.get("user_id", ""),
            requirement_text=data.get("requirement_text", ""),
            language=data.get("language", ""),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển Request entity thành dictionary"""
        result = {
            "user_id": ObjectId(self.user_id) if self.user_id else None,
            "requirement_text": self.requirement_text,
            "language": self.language,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển Request entity thành response dictionary"""
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "requirement_text": self.requirement_text,
            "language": self.language,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"Request(id={self.id}, language={self.language}, user_id={self.user_id})"
