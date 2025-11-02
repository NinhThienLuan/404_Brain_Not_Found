"""
CodeReview Entity - Đại diện cho code review result
"""
from datetime import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class CodeReview:
    """
    CodeReview Entity - Domain model cho code review
    """
    code: str
    language: str
    overall_score: float
    user_id: str
    id: Optional[str] = None
    review_type: str = "general"
    issues: List[Dict] = field(default_factory=list)
    summary: Optional[str] = None
    improvements: List[str] = field(default_factory=list)
    additional_notes: Optional[str] = None
    model: str = "gemini-1.5-flash"
    success: bool = True
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'CodeReview':
        """Tạo CodeReview entity từ dictionary"""
        return CodeReview(
            id=str(data["_id"]) if "_id" in data else None,
            code=data["code"],
            language=data["language"],
            overall_score=data["overall_score"],
            user_id=data["user_id"],
            review_type=data.get("review_type", "general"),
            issues=data.get("issues", []),
            summary=data.get("summary"),
            improvements=data.get("improvements", []),
            additional_notes=data.get("additional_notes"),
            model=data.get("model", "gemini-1.5-flash"),
            success=data.get("success", True),
            error_message=data.get("error_message"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển CodeReview entity thành dictionary"""
        result = {
            "code": self.code,
            "language": self.language,
            "overall_score": self.overall_score,
            "user_id": self.user_id,
            "review_type": self.review_type,
            "issues": self.issues,
            "summary": self.summary,
            "improvements": self.improvements,
            "additional_notes": self.additional_notes,
            "model": self.model,
            "success": self.success,
            "error_message": self.error_message,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển CodeReview entity thành response dictionary"""
        return {
            "_id": self.id,
            "code": self.code,
            "language": self.language,
            "overall_score": self.overall_score,
            "user_id": self.user_id,
            "review_type": self.review_type,
            "issues": self.issues,
            "summary": self.summary,
            "improvements": self.improvements,
            "additional_notes": self.additional_notes,
            "model": self.model,
            "success": self.success,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"CodeReview(id={self.id}, score={self.overall_score}, language={self.language})"

