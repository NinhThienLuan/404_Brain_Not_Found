"""
Conservation Entity - Đại diện cho conservation/conversation
Khớp với structure thực tế trong MongoDB
Lưu ý: Collection name là "conservations" (không phải "conversations")
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class Conservation:
    """
    Conservation Entity - Domain model cho conservations
    """
    title: str
    goal: str
    message_count: int = 0
    facts: List[str] = field(default_factory=list)
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'Conservation':
        """Tạo Conservation entity từ dictionary"""
        return Conservation(
            id=str(data["_id"]) if "_id" in data else None,
            title=data.get("title", ""),
            goal=data.get("goal", ""),
            message_count=data.get("messageCount", 0),
            facts=data.get("facts", []),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển Conservation entity thành dictionary"""
        result = {
            "title": self.title,
            "goal": self.goal,
            "messageCount": self.message_count,
            "facts": self.facts,
            "createdAt": self.created_at or datetime.utcnow(),
            "updatedAt": self.updated_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển Conservation entity thành response dictionary"""
        return {
            "_id": self.id,
            "title": self.title,
            "goal": self.goal,
            "messageCount": self.message_count,
            "facts": self.facts,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"Conservation(id={self.id}, title={self.title}, messages={self.message_count})"

