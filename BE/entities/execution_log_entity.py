"""
ExecutionLog Entity - Đại diện cho execution log
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class ExecutionLog:
    """
    ExecutionLog Entity - Domain model cho execution logs
    """
    code: str
    language: str
    user_id: str
    id: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None  # milliseconds
    status: str = "pending"  # pending, success, error
    code_generation_id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'ExecutionLog':
        """Tạo ExecutionLog entity từ dictionary"""
        return ExecutionLog(
            id=str(data["_id"]) if "_id" in data else None,
            code=data["code"],
            language=data["language"],
            user_id=data["user_id"],
            output=data.get("output"),
            error=data.get("error"),
            execution_time=data.get("execution_time"),
            status=data.get("status", "pending"),
            code_generation_id=data.get("code_generation_id"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển ExecutionLog entity thành dictionary"""
        result = {
            "code": self.code,
            "language": self.language,
            "user_id": self.user_id,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "status": self.status,
            "code_generation_id": self.code_generation_id,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển ExecutionLog entity thành response dictionary"""
        return {
            "_id": self.id,
            "code": self.code,
            "language": self.language,
            "user_id": self.user_id,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "status": self.status,
            "code_generation_id": self.code_generation_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"ExecutionLog(id={self.id}, status={self.status}, language={self.language})"

