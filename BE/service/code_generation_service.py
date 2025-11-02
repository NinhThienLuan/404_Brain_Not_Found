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
    
    def get_by_language(self, language: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code generations theo language"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_language(language, skip=skip, limit=page_size)
        total = self.repo.count({"language": language})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def get_successful(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy các code generation thành công"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_successful(skip=skip, limit=page_size)
        total = self.repo.count({"success": True})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

