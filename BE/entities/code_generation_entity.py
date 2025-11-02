"""
CodeGeneration Entity - Đại diện cho code generation request/response
"""
from datetime import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class CodeGeneration:
    """
    CodeGeneration Entity - Domain model cho code generation
    Khớp với structure thực tế trong MongoDB
    """
    request_id: str
    files_json: List[Dict] = field(default_factory=list)
    id: Optional[str] = None
    run_instructions: Optional[str] = None
    status: str = "pending"  # pending, success, error
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'CodeGeneration':
        """Tạo CodeGeneration entity từ dictionary"""
        return CodeGeneration(
            id=str(data["_id"]) if "_id" in data else None,
            request_id=str(data["request_id"]) if isinstance(data.get("request_id"), ObjectId) else data.get("request_id", ""),
            files_json=data.get("files_json", []),
            run_instructions=data.get("run_instructions"),
            status=data.get("status", "pending"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self, include_id: bool = True) -> dict:
        """Chuyển CodeGeneration entity thành dictionary"""
        result = {
            "request_id": ObjectId(self.request_id) if self.request_id else None,
            "files_json": self.files_json,
            "run_instructions": self.run_instructions,
            "status": self.status,
            "created_at": self.created_at or datetime.utcnow()
        }
        
        if include_id and self.id:
            result["_id"] = ObjectId(self.id)
        
        return result
    
    def to_response(self) -> dict:
        """Chuyển CodeGeneration entity thành response dictionary"""
        return {
            "_id": self.id,
            "request_id": self.request_id,
            "files_json": self.files_json,
            "run_instructions": self.run_instructions,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"CodeGeneration(id={self.id}, request_id={self.request_id}, status={self.status})"

