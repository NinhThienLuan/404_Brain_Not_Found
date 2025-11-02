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
    
    def find_by_type(self, request_type: str, skip: int = 0, limit: int = 100) -> List[Request]:
        """Tìm requests theo type"""
        return self.find_all(skip=skip, limit=limit, filter_query={"request_type": request_type})
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Request]:
        """Tìm requests theo status"""
        return self.find_all(skip=skip, limit=limit, filter_query={"status": status})
    
    def find_pending(self, skip: int = 0, limit: int = 100) -> List[Request]:
        """Lấy các requests đang pending"""
        return self.find_by_status("pending", skip, limit)
    
    def find_completed(self, skip: int = 0, limit: int = 100) -> List[Request]:
        """Lấy các requests đã hoàn thành"""
        return self.find_by_status("completed", skip, limit)
    
    def find_by_user_and_type(self, user_id: str, request_type: str, skip: int = 0, limit: int = 100) -> List[Request]:
        """Tìm requests của user theo type"""
        return self.find_all(
            skip=skip,
            limit=limit,
            filter_query={"user_id": user_id, "request_type": request_type}
        )

