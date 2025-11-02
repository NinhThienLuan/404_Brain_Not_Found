"""
Context Entity - Lưu trữ context đã được parse
"""
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class Context:
    """
    Context Entity - Đại diện cho một context đã được parse
    
    Chứa thông tin:
    - Raw text từ user
    - Parsed JSON (topic, functions, input, output...)
    - Metadata
    """
    session_id: str
    raw_text: str
    parsed_json: Dict[str, Any]
    parsing_model: str = "gemini-2.5-flash"
    confidence_score: float = 0.0
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'Context':
        """Tạo Context từ MongoDB document"""
        return Context(
            id=str(data["_id"]) if "_id" in data else None,
            session_id=data["session_id"],
            raw_text=data["raw_text"],
            parsed_json=data["parsed_json"],
            parsing_model=data.get("parsing_model", "gemini-2.5-flash"),
            confidence_score=data.get("confidence_score", 0.0),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển Context thành dictionary"""
        result = {
            "session_id": self.session_id,
            "raw_text": self.raw_text,
            "parsed_json": self.parsed_json,
            "parsing_model": self.parsing_model,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển thành response cho API"""
        return {
            "_id": self.id,
            "session_id": self.session_id,
            "raw_text": self.raw_text,
            "parsed_json": self.parsed_json,
            "parsing_model": self.parsing_model,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

