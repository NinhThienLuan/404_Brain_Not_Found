"""
ChatRoom Service - Business logic cho ChatRoom
"""
from typing import List, Optional
from datetime import datetime
from BE.entities.chat_room_entity import ChatRoom
from BE.repository.chat_room_repo import ChatRoomRepository
from BE.service.base_service import BaseService


class ChatRoomService(BaseService[ChatRoom]):
    """Service xử lý business logic cho ChatRoom"""
    
    def __init__(self):
        self.repo = ChatRoomRepository()
        super().__init__(self.repo)
    
    def create_room(self, user_id: str, title: str = None) -> ChatRoom:
        """
        Tạo phòng chat mới
        
        Args:
            user_id: ID của user
            title: Tiêu đề phòng chat (tự động generate nếu không có)
            
        Returns:
            ChatRoom: Phòng chat mới
        """
        # Tự động generate title nếu không có
        if not title:
            title = f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        
        room = ChatRoom(
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return self.create(room)
    
    def get_user_rooms(self, user_id: str, limit: int = 50) -> List[ChatRoom]:
        """
        Lấy tất cả phòng chat của user
        
        Args:
            user_id: ID của user
            limit: Số lượng phòng tối đa
            
        Returns:
            List[ChatRoom]: Danh sách phòng chat
        """
        return self.repo.get_rooms_by_user(user_id, limit)
    
    def update_title(self, room_id: str, new_title: str) -> Optional[ChatRoom]:
        """
        Cập nhật tiêu đề phòng chat
        
        Args:
            room_id: ID của phòng chat
            new_title: Tiêu đề mới
            
        Returns:
            Optional[ChatRoom]: Phòng chat sau khi cập nhật
        """
        if not new_title or len(new_title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        
        return self.repo.update_room_title(room_id, new_title)
    
    def delete_room(self, room_id: str) -> bool:
        """
        Xóa phòng chat (soft delete)
        
        Args:
            room_id: ID của phòng chat
            
        Returns:
            bool: True nếu xóa thành công
        """
        return self.repo.soft_delete_room(room_id)
