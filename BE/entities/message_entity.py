"""
Message Entity - Đại diện cho message trong conversation
Khớp với structure thực tế trong MongoDB
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class Message:
    """
    Message Entity - Domain model cho messages
    """
    conversation_id: str  # Link to conservation
    sender: str  # "system" hoặc "user"
    text: str
    type: str = "text"  # Type of message
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    v: int = 0  # __v field từ MongoDB
    
    @staticmethod
    def from_dict(data: dict) -> 'Message':
        """Tạo Message entity từ dictionary"""
        return Message(
            id=str(data["_id"]) if "_id" in data else None,
            conversation_id=str(data["conversationId"]) if isinstance(data.get("conversationId"), ObjectId) else data.get("conversationId", ""),
            sender=data.get("sender", "user"),
            text=data.get("text", ""),
            type=data.get("type", "text"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
            v=data.get("__v", 0)
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển Message entity thành dictionary"""
        result = {
            "conversationId": ObjectId(self.conversation_id) if self.conversation_id else None,
            "sender": self.sender,
            "text": self.text,
            "type": self.type,
            "createdAt": self.created_at or datetime.utcnow(),
            "updatedAt": self.updated_at or datetime.utcnow(),
            "__v": self.v
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển Message entity thành response dictionary"""
        return {
            "_id": self.id,
            "conversationId": self.conversation_id,
            "sender": self.sender,
            "text": self.text,
            "type": self.type,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "__v": self.v
        }
    
    def __repr__(self) -> str:
        return f"Message(id={self.id}, sender={self.sender}, conversation={self.conversation_id})"
