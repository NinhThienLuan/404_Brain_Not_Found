"""
<<<<<<< HEAD
ChatRoom Repository
"""
from typing import List
from BE.repository.base_repo import BaseRepository
from BE.entities.chat_room_entity import ChatRoom


class ChatRoomRepository(BaseRepository[ChatRoom]):
    """Repository cho ChatRoom collection"""
=======
ChatRoom Repository - Data access layer cho ChatRoom
"""
from typing import List, Optional
from bson import ObjectId
from BE.entities.chat_room_entity import ChatRoom
from BE.repository.base_repo import BaseRepository


class ChatRoomRepository(BaseRepository[ChatRoom]):
    """Repository cho ChatRoom với các operations cụ thể"""
>>>>>>> 4de381ce979ed4ae2fe2d771c3b6737ec53733f5
    
    def __init__(self):
        super().__init__("chat_rooms", ChatRoom)
    
<<<<<<< HEAD
    def find_active(self, skip: int = 0, limit: int = 100) -> List[ChatRoom]:
        """Lấy các chat rooms đang active"""
        return self.find_all(skip=skip, limit=limit, filter_query={"is_active": True})
    
    def find_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ChatRoom]:
        """Tìm chat rooms của user"""
        return self.find_all(skip=skip, limit=limit, filter_query={"user_id": user_id})

=======
    def get_rooms_by_user(self, user_id: str, limit: int = 50) -> List[ChatRoom]:
        """
        Lấy tất cả phòng chat của một user
        
        Args:
            user_id: ID của user
            limit: Số lượng phòng tối đa
            
        Returns:
            List[ChatRoom]: Danh sách phòng chat
        """
        try:
            cursor = self.collection.find(
                {"user_id": user_id, "is_active": True}
            ).sort("updated_at", -1).limit(limit)
            
            return [ChatRoom.from_dict(doc) for doc in cursor]
        except Exception as e:
            print(f"Error getting chat rooms by user: {e}")
            return []
    
    def update_room_title(self, room_id: str, new_title: str) -> Optional[ChatRoom]:
        """
        Cập nhật tiêu đề phòng chat
        
        Args:
            room_id: ID của phòng chat
            new_title: Tiêu đề mới
            
        Returns:
            Optional[ChatRoom]: Phòng chat sau khi cập nhật
        """
        from datetime import datetime
        
        try:
            result = self.collection.find_one_and_update(
                {"_id": ObjectId(room_id)},
                {"$set": {
                    "title": new_title,
                    "updated_at": datetime.utcnow()
                }},
                return_document=True
            )
            
            if result:
                return ChatRoom.from_dict(result)
            return None
        except Exception as e:
            print(f"Error updating room title: {e}")
            return None
    
    def soft_delete_room(self, room_id: str) -> bool:
        """
        Xóa mềm phòng chat (đánh dấu is_active = False)
        
        Args:
            room_id: ID của phòng chat
            
        Returns:
            bool: True nếu xóa thành công
        """
        from datetime import datetime
        
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(room_id)},
                {"$set": {
                    "is_active": False,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error soft deleting room: {e}")
            return False
>>>>>>> 4de381ce979ed4ae2fe2d771c3b6737ec53733f5
