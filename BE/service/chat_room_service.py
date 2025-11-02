"""
ChatRoom Service
"""
from typing import Dict
from BE.service.base_service import BaseService
from BE.repository.chat_room_repo import ChatRoomRepository
from BE.entities.chat_room_entity import ChatRoom


class ChatRoomService(BaseService[ChatRoom]):
    """Service cho ChatRoom"""
    
    def __init__(self):
        super().__init__(ChatRoomRepository())
    
    def get_active(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy các chat rooms đang active"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_active(skip=skip, limit=page_size)
        total = self.repo.count({"is_active": True})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

