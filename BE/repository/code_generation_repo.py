"""
CodeGeneration Repository
"""
from typing import List, Optional
from BE.repository.base_repo import BaseRepository
from BE.entities.code_generation_entity import CodeGeneration


class CodeGenerationRepository(BaseRepository[CodeGeneration]):
    """Repository cho CodeGeneration collection"""
    
    def __init__(self):
        super().__init__("code_generations", CodeGeneration)
    
    def find_by_language(self, language: str, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Tìm code generations theo language"""
        return self.find_all(skip=skip, limit=limit, filter_query={"language": language})
    
    def find_successful(self, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Lấy các code generation thành công"""
        return self.find_all(skip=skip, limit=limit, filter_query={"success": True})
    
    def find_by_user_and_language(self, user_id: str, language: str, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Tìm code generations của user theo language"""
        return self.find_all(
            skip=skip,
            limit=limit,
            filter_query={"user_id": user_id, "language": language}
        )

