"""
Message Service - Business logic cho Message
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from BE.entities.message_entity import Message
from BE.repository.message_repo import MessageRepository
from BE.service.base_service import BaseService


class MessageService(BaseService[Message]):
    """Service xử lý business logic cho Message"""
    
    def __init__(self):
        self.repo = MessageRepository()
        super().__init__(self.repo)
    
    def send_message(
        self,
        chat_room_id: str,
        content: str,
        sender_type: str = "user",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Gửi tin nhắn mới
        
        Args:
            chat_room_id: ID của phòng chat
            content: Nội dung tin nhắn
            sender_type: Loại người gửi ("user" hoặc "ai")
            metadata: Dữ liệu bổ sung
            
        Returns:
            Message: Tin nhắn mới
        """
        if not content or len(content.strip()) == 0:
            raise ValueError("Message content cannot be empty")
        
        if sender_type not in ["user", "ai"]:
            raise ValueError("sender_type must be 'user' or 'ai'")
        
        message = Message(
            chat_room_id=chat_room_id,
            content=content,
            sender_type=sender_type,
            created_at=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        return self.create(message)
    
    def get_room_messages(
        self,
        chat_room_id: str,
        limit: int = 100,
        skip: int = 0
    ) -> List[Message]:
        """
        Lấy tin nhắn trong phòng chat
        
        Args:
            chat_room_id: ID của phòng chat
            limit: Số lượng tin nhắn tối đa
            skip: Số lượng tin nhắn bỏ qua
            
        Returns:
            List[Message]: Danh sách tin nhắn
        """
        return self.repo.get_messages_by_room(chat_room_id, limit, skip)
    
    def get_last_message(self, chat_room_id: str) -> Optional[Message]:
        """
        Lấy tin nhắn cuối cùng
        
        Args:
            chat_room_id: ID của phòng chat
            
        Returns:
            Optional[Message]: Tin nhắn cuối cùng
        """
        return self.repo.get_last_message(chat_room_id)
    
    def count_messages(self, chat_room_id: str) -> int:
        """
        Đếm số lượng tin nhắn trong phòng
        
        Args:
            chat_room_id: ID của phòng chat
            
        Returns:
            int: Số lượng tin nhắn
        """
        return self.repo.count_messages_in_room(chat_room_id)
