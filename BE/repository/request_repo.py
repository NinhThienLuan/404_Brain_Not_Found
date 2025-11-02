"""
Request Repository
"""
from typing import List
from BE.repository.base_repo import BaseRepository
from BE.entities.request_entity import Request


class RequestRepository(BaseRepository[Request]):
    """Repository cho Request collection"""
    
    def __init__(self):
        super().__init__("requests", Request)
    
    def find_by_language(self, language: str, skip: int = 0, limit: int = 100) -> List[Request]:
        """Tìm requests theo language"""
        return self.find_all(skip=skip, limit=limit, filter_query={"language": language})
    
    def find_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Request]:
        """Tìm requests theo user_id"""
        return self.find_all(skip=skip, limit=limit, filter_query={"user_id": user_id})
