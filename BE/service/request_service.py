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
    
    def get_by_type(self, request_type: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy requests theo type"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_type(request_type, skip=skip, limit=page_size)
        total = self.repo.count({"request_type": request_type})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def get_by_status(self, status: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy requests theo status"""
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
    
    def get_pending(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy các requests đang pending"""
        return self.get_by_status("pending", page, page_size)
    
    def get_completed(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy các requests đã hoàn thành"""
        return self.get_by_status("completed", page, page_size)

