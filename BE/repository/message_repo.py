"""
Message Repository
"""
from typing import List
from bson import ObjectId
from BE.repository.base_repo import BaseRepository
from BE.entities.message_entity import Message


class MessageRepository(BaseRepository[Message]):
    """Repository cho Messages collection"""
    
    def __init__(self):
        super().__init__("messages", Message)
    
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

