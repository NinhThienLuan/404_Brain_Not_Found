"""
ExecutionLog Entity - Đại diện cho execution log
Khớp với structure thực tế trong MongoDB
"""
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class ExecutionLog:
    """
    ExecutionLog Entity - Domain model cho execution logs
    """
    gen_id: str
    compile_result: Dict
    test_result: Dict
    lint_result: Dict
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'ExecutionLog':
        """Tạo ExecutionLog entity từ dictionary"""
        return ExecutionLog(
            id=str(data["_id"]) if "_id" in data else None,
            gen_id=str(data["gen_id"]) if isinstance(data.get("gen_id"), ObjectId) else data.get("gen_id", ""),
            compile_result=data.get("compile_result", {}),
            test_result=data.get("test_result", {}),
            lint_result=data.get("lint_result", {}),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển ExecutionLog entity thành dictionary"""
        result = {
            "gen_id": ObjectId(self.gen_id) if self.gen_id else None,
            "compile_result": self.compile_result,
            "test_result": self.test_result,
            "lint_result": self.lint_result,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển ExecutionLog entity thành response dictionary"""
        return {
            "_id": self.id,
            "gen_id": self.gen_id,
            "compile_result": self.compile_result,
            "test_result": self.test_result,
            "lint_result": self.lint_result,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"ExecutionLog(id={self.id}, gen_id={self.gen_id})"
