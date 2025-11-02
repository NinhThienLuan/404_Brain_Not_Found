"""
Message Repository - Data access layer cho Message
"""
from typing import List, Optional
from bson import ObjectId
from BE.entities.message_entity import Message
from BE.repository.base_repo import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository cho Message với các operations cụ thể"""
    
    def __init__(self):
        super().__init__("messages", Message)
    
    def get_messages_by_room(
        self, 
        chat_room_id: str, 
        limit: int = 100,
        skip: int = 0
    ) -> List[Message]:
        """
        Lấy tin nhắn trong một phòng chat
        
        Args:
            chat_room_id: ID của phòng chat
            limit: Số lượng tin nhắn tối đa
            skip: Số lượng tin nhắn bỏ qua (cho pagination)
            
        Returns:
            List[Message]: Danh sách tin nhắn
        """
        try:
            cursor = self.collection.find(
                {"chat_room_id": chat_room_id}
            ).sort("created_at", 1).skip(skip).limit(limit)
            
            return [Message.from_dict(doc) for doc in cursor]
        except Exception as e:
            print(f"Error getting messages by room: {e}")
            return []
    
    def get_last_message(self, chat_room_id: str) -> Optional[Message]:
        """
        Lấy tin nhắn cuối cùng trong phòng chat
        
        Args:
            chat_room_id: ID của phòng chat
            
        Returns:
            Optional[Message]: Tin nhắn cuối cùng
        """
        try:
            doc = self.collection.find_one(
                {"chat_room_id": chat_room_id},
                sort=[("created_at", -1)]
            )
            
            if doc:
                return Message.from_dict(doc)
            return None
        except Exception as e:
            print(f"Error getting last message: {e}")
            return None
    
    def count_messages_in_room(self, chat_room_id: str) -> int:
        """
        Đếm số lượng tin nhắn trong phòng chat
        
        Args:
            chat_room_id: ID của phòng chat
            
        Returns:
            int: Số lượng tin nhắn
        """
        try:
            return self.collection.count_documents({"chat_room_id": chat_room_id})
        except Exception as e:
            print(f"Error counting messages: {e}")
            return 0
