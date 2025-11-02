"""
ExecutionLog Service
"""
from typing import Dict
from BE.service.base_service import BaseService
from BE.repository.execution_log_repo import ExecutionLogRepository
from BE.entities.execution_log_entity import ExecutionLog


class ExecutionLogService(BaseService[ExecutionLog]):
    """Service cho ExecutionLog"""
    
    def __init__(self):
        super().__init__(ExecutionLogRepository())
    
    def get_by_status(self, status: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy execution logs theo status"""
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
    
    def get_successful(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy các execution thành công"""
        return self.get_by_status("success", page, page_size)
    
    def get_failed(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy các execution thất bại"""
        return self.get_by_status("error", page, page_size)

