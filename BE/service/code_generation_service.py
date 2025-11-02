"""
CodeGeneration Service
"""
from typing import Dict
from BE.service.base_service import BaseService
from BE.repository.code_generation_repo import CodeGenerationRepository
from BE.entities.code_generation_entity import CodeGeneration


class CodeGenerationService(BaseService[CodeGeneration]):
    """Service cho CodeGeneration"""
    
    def __init__(self):
        super().__init__(CodeGenerationRepository())
    
    def get_by_request(self, request_id: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code generations theo request_id"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_request(request_id, skip=skip, limit=page_size)
        total = self.repo.count({"request_id": request_id})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def get_by_status(self, status: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code generations theo status"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_status(status, skip=skip, limit=page_size)
        total = self.repo.count({"status": status})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
