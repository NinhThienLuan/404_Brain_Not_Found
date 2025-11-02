"""
Message Entity - Đại diện cho tin nhắn trong phòng chat
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class Message:
    """
    Message Entity - Domain model cho tin nhắn
    
    Đại diện cho một tin nhắn trong phòng chat
    """
    chat_room_id: str  # ID của phòng chat
    content: str  # Nội dung tin nhắn
    sender_type: str  # "user" hoặc "ai"
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    metadata: Optional[dict] = None  # Dữ liệu bổ sung (code, language, etc.)
    
    @staticmethod
    def from_dict(data: dict) -> 'Message':
        """
        Tạo Message entity từ dictionary (thường là từ MongoDB)
        
        Args:
            data: Dictionary chứa data của message
            
        Returns:
            Message: Message entity
        """
        return Message(
            id=str(data["_id"]) if "_id" in data else None,
            chat_room_id=str(data["chat_room_id"]),
            content=data["content"],
            sender_type=data["sender_type"],
            created_at=data.get("created_at"),
            metadata=data.get("metadata")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """
        Chuyển Message entity thành dictionary
        
        Args:
            include_id: Có include _id field không (dùng khi insert thì False)
            
        Returns:
            dict: Dictionary representation của Message
        """
        result = {
            "chat_room_id": self.chat_room_id,
            "content": self.content,
            "sender_type": self.sender_type,
            "created_at": self.created_at or datetime.utcnow(),
            "metadata": self.metadata or {}
        }
        
        if include_id and self.id:
            from bson import ObjectId
            result["_id"] = ObjectId(self.id)
            
        return result
    
    def __repr__(self) -> str:
        return f"Message(id={self.id}, chat_room_id={self.chat_room_id}, sender_type={self.sender_type})"
