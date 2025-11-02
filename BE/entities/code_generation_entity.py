"""
CodeGeneration Entity - Đại diện cho code generation request/response
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class CodeGeneration:
    """
    CodeGeneration Entity - Domain model cho code generation
    """
    prompt: str
    language: str
    generated_code: str
    user_id: str
    id: Optional[str] = None
    framework: Optional[str] = None
    additional_context: Optional[str] = None
    explanation: Optional[str] = None
    model: str = "gemini-2.5-flash"
    success: bool = True
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'CodeGeneration':
        """Tạo CodeGeneration entity từ dictionary"""
        return CodeGeneration(
            id=str(data["_id"]) if "_id" in data else None,
            prompt=data["prompt"],
            language=data["language"],
            generated_code=data["generated_code"],
            user_id=data["user_id"],
            framework=data.get("framework"),
            additional_context=data.get("additional_context"),
            explanation=data.get("explanation"),
            model=data.get("model", "gemini-2.5-flash"),
            success=data.get("success", True),
            error_message=data.get("error_message"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển CodeGeneration entity thành dictionary"""
        result = {
            "prompt": self.prompt,
            "language": self.language,
            "generated_code": self.generated_code,
            "user_id": self.user_id,
            "framework": self.framework,
            "additional_context": self.additional_context,
            "explanation": self.explanation,
            "model": self.model,
            "success": self.success,
            "error_message": self.error_message,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển CodeGeneration entity thành response dictionary"""
        return {
            "_id": self.id,
            "prompt": self.prompt,
            "language": self.language,
            "generated_code": self.generated_code,
            "user_id": self.user_id,
            "framework": self.framework,
            "additional_context": self.additional_context,
            "explanation": self.explanation,
            "model": self.model,
            "success": self.success,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"CodeGeneration(id={self.id}, language={self.language}, user={self.user_id})"

