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
    
    def find_by_gen_id(self, gen_id: str, skip: int = 0, limit: int = 100) -> List[ExecutionLog]:
        """Tìm execution logs theo gen_id"""
        return self.find_all(skip=skip, limit=limit, filter_query={"gen_id": gen_id})
