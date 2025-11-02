"""
CodeReview Entity - Đại diện cho code review result
Khớp với structure thực tế trong MongoDB
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class CodeReview:
    """
    CodeReview Entity - Domain model cho code review
    """
    gen_id: str
    review_markdown: str
    score: int  # 0-10
    id: Optional[str] = None
    summary: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'CodeReview':
        """Tạo CodeReview entity từ dictionary"""
        return CodeReview(
            id=str(data["_id"]) if "_id" in data else None,
            gen_id=str(data["gen_id"]) if isinstance(data.get("gen_id"), ObjectId) else data.get("gen_id", ""),
            review_markdown=data.get("review_markdown", ""),
            score=data.get("score", 0),
            summary=data.get("summary"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển CodeReview entity thành dictionary"""
        result = {
            "gen_id": ObjectId(self.gen_id) if self.gen_id else None,
            "review_markdown": self.review_markdown,
            "score": self.score,
            "summary": self.summary,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển CodeReview entity thành response dictionary"""
        return {
            "_id": self.id,
            "gen_id": self.gen_id,
            "review_markdown": self.review_markdown,
            "score": self.score,
            "summary": self.summary,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"CodeReview(id={self.id}, score={self.score}, gen_id={self.gen_id})"
