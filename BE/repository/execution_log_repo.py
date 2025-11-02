"""
ExecutionLog Repository
"""
from typing import List
from BE.repository.base_repo import BaseRepository
from BE.entities.execution_log_entity import ExecutionLog


class ExecutionLogRepository(BaseRepository[ExecutionLog]):
    """Repository cho ExecutionLog collection"""
    
    def __init__(self):
        super().__init__("execution_logs", ExecutionLog)
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[ExecutionLog]:
        """Tìm execution logs theo status"""
        return self.find_all(skip=skip, limit=limit, filter_query={"status": status})
    
    def find_by_code_generation(self, code_generation_id: str, skip: int = 0, limit: int = 100) -> List[ExecutionLog]:
        """Tìm execution logs theo code_generation_id"""
        return self.find_all(
            skip=skip,
            limit=limit,
            filter_query={"code_generation_id": code_generation_id}
        )
    
    def find_successful(self, skip: int = 0, limit: int = 100) -> List[ExecutionLog]:
        """Lấy các execution thành công"""
        return self.find_by_status("success", skip, limit)
    
    def find_failed(self, skip: int = 0, limit: int = 100) -> List[ExecutionLog]:
        """Lấy các execution thất bại"""
        return self.find_by_status("error", skip, limit)

