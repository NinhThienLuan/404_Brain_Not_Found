"""
Request Service
"""
from typing import Dict
from BE.service.base_service import BaseService
from BE.repository.request_repo import RequestRepository
from BE.entities.request_entity import Request


class RequestService(BaseService[Request]):
    """Service cho Request"""
    
    def __init__(self):
        super().__init__(RequestRepository())
    
    def get_by_language(self, language: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy requests theo language"""
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
