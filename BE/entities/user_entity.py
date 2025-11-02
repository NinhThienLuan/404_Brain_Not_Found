"""
User Entity - Đại diện cho User object trong business logic
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class User:
    """
    User Entity - Domain model cho User
    
    Đây là object thuần túy đại diện cho User trong business logic,
    không phụ thuộc vào database hay framework nào.
    """
    name: str
    email: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        """
        Tạo User entity từ dictionary (thường là từ MongoDB)
        
        Args:
            data: Dictionary chứa data của user
            
        Returns:
            User: User entity
        """
        return User(
            id=str(data["_id"]) if "_id" in data else None,
            name=data["name"],
            email=data["email"],
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """
        Chuyển User entity thành dictionary
        
        Args:
            include_id: Có include _id field không (dùng khi insert thì False)
            
        Returns:
            dict: Dictionary representation của User
        """
        result = {
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """
        Chuyển User entity thành response dictionary cho API
        
        Returns:
            dict: Response-friendly dictionary
        """
        return {
            "_id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
    
    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

