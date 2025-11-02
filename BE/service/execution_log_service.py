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
    
    def get_by_gen_id(self, gen_id: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy execution logs theo gen_id"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_gen_id(gen_id, skip=skip, limit=page_size)
        total = self.repo.count({"gen_id": gen_id})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
