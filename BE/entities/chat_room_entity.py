"""
<<<<<<< HEAD
ChatRoom Entity - Đại diện cho chat room
Khớp với structure thực tế trong MongoDB
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from bson import ObjectId
=======
ChatRoom Entity - Đại diện cho phòng chat trong business logic
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
>>>>>>> 4de381ce979ed4ae2fe2d771c3b6737ec53733f5


@dataclass
class ChatRoom:
    """
<<<<<<< HEAD
    ChatRoom Entity - Domain model cho chat rooms
    """
    user_id: str
    title: str
    id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'ChatRoom':
        """Tạo ChatRoom entity từ dictionary"""
        return ChatRoom(
            id=str(data["_id"]) if "_id" in data else None,
            user_id=str(data["user_id"]) if isinstance(data.get("user_id"), ObjectId) else data.get("user_id", ""),
            title=data.get("title", ""),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển ChatRoom entity thành dictionary"""
        result = {
            "user_id": self.user_id,  # Keep as string in DB
            "title": self.title,
            "is_active": self.is_active,
            "created_at": self.created_at or datetime.utcnow(),
            "updated_at": self.updated_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển ChatRoom entity thành response dictionary"""
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"ChatRoom(id={self.id}, title={self.title}, user_id={self.user_id})"

=======
    ChatRoom Entity - Domain model cho phòng chat
    
    Đại diện cho một phòng chat/conversation trong hệ thống
    """
    user_id: str  # ID của user sở hữu room này
    title: str  # Tiêu đề của phòng chat
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True  # Trạng thái phòng chat
    
    @staticmethod
    def from_dict(data: dict) -> 'ChatRoom':
        """
        Tạo ChatRoom entity từ dictionary (thường là từ MongoDB)
        
        Args:
            data: Dictionary chứa data của chat room
            
        Returns:
            ChatRoom: ChatRoom entity
        """
        return ChatRoom(
            id=str(data["_id"]) if "_id" in data else None,
            user_id=str(data["user_id"]),
            title=data["title"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            is_active=data.get("is_active", True)
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """
        Chuyển ChatRoom entity thành dictionary
        
        Args:
            include_id: Có include _id field không (dùng khi insert thì False)
            
        Returns:
            dict: Dictionary representation của ChatRoom
        """
        result = {
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at or datetime.utcnow(),
            "updated_at": self.updated_at or datetime.utcnow(),
            "is_active": self.is_active
        }
        
        if include_id and self.id:
            from bson import ObjectId
            result["_id"] = ObjectId(self.id)
            
        return result
    
    def __repr__(self) -> str:
        return f"ChatRoom(id={self.id}, title={self.title}, user_id={self.user_id})"
>>>>>>> 4de381ce979ed4ae2fe2d771c3b6737ec53733f5
