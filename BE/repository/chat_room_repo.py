"""
ChatRoom Repository
"""
from typing import List
from BE.repository.base_repo import BaseRepository
from BE.entities.chat_room_entity import ChatRoom


class ChatRoomRepository(BaseRepository[ChatRoom]):
    """Repository cho ChatRoom collection"""
    
    def __init__(self):
        super().__init__("chat_rooms", ChatRoom)
    
    def find_active(self, skip: int = 0, limit: int = 100) -> List[ChatRoom]:
        """Lấy các chat rooms đang active"""
        return self.find_all(skip=skip, limit=limit, filter_query={"is_active": True})
    
    def find_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ChatRoom]:
        """Tìm chat rooms của user"""
        return self.find_all(skip=skip, limit=limit, filter_query={"user_id": user_id})

