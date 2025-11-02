"""
CodeGeneration Repository
"""
from typing import List
from BE.repository.base_repo import BaseRepository
from BE.entities.code_generation_entity import CodeGeneration


class CodeGenerationRepository(BaseRepository[CodeGeneration]):
    """Repository cho CodeGeneration collection"""
    
    def __init__(self):
        super().__init__("code_generations", CodeGeneration)
    
    def find_by_request(self, request_id: str, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Tìm code generations theo request_id"""
        return self.find_all(skip=skip, limit=limit, filter_query={"request_id": request_id})
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Tìm code generations theo status"""
        return self.find_all(skip=skip, limit=limit, filter_query={"status": status})
    
    def find_successful(self, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Lấy các code generation thành công"""
        return self.find_by_status("success", skip, limit)
