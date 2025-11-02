"""
<<<<<<< HEAD
Message Repository
"""
from typing import List
from bson import ObjectId
from BE.repository.base_repo import BaseRepository
from BE.entities.message_entity import Message


class MessageRepository(BaseRepository[Message]):
    """Repository cho Messages collection"""
=======
Message Repository - Data access layer cho Message
"""
from typing import List, Optional
from bson import ObjectId
from BE.entities.message_entity import Message
from BE.repository.base_repo import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository cho Message với các operations cụ thể"""
>>>>>>> 4de381ce979ed4ae2fe2d771c3b6737ec53733f5
    
    def __init__(self):
        super().__init__("messages", Message)
    
<<<<<<< HEAD
    def find_by_conversation(self, conversation_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """
        Lấy tất cả messages của một conversation
        
        Args:
            conversation_id: ID của conversation
            skip: Số lượng bỏ qua
            limit: Số lượng tối đa
            
        Returns:
            List[Message]: Danh sách messages
        """
        try:
            obj_id = ObjectId(conversation_id)
            return self.find_all(
                skip=skip,
                limit=limit,
                filter_query={"conversationId": obj_id}
            )
        except:
            return []
    
    def find_by_sender(self, sender: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """Lấy messages theo sender (system/user)"""
        return self.find_all(skip=skip, limit=limit, filter_query={"sender": sender})
    
    def count_by_conversation(self, conversation_id: str) -> int:
        """Đếm số messages trong một conversation"""
        try:
            obj_id = ObjectId(conversation_id)
            return self.count({"conversationId": obj_id})
        except:
            return 0
    
    def delete_by_conversation(self, conversation_id: str) -> int:
        """
        Xóa tất cả messages của một conversation
        
        Returns:
            int: Số lượng messages đã xóa
        """
        try:
            obj_id = ObjectId(conversation_id)
            result = self.collection.delete_many({"conversationId": obj_id})
            return result.deleted_count
        except:
            return 0

=======
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
>>>>>>> 4de381ce979ed4ae2fe2d771c3b6737ec53733f5
