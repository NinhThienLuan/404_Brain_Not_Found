
from typing import Dict, Optional
from datetime import datetime
from BE.service.base_service import BaseService
from BE.repository.message_repo import MessageRepository
from BE.repository.conservation_repo import ConservationRepository
from BE.entities.message_entity import Message


class MessageService(BaseService[Message]):
    """Service cho Message với business logic"""
    
    def __init__(self):
        super().__init__(MessageRepository())
        self.conservation_repo = ConservationRepository()
    
    def create_message(self, conversation_id: str, sender: str, text: str, message_type: str = "text") -> Message:
        """
        Tạo message mới và tự động update conservation message count
        
        Args:
            conversation_id: ID của conversation
            sender: "system" hoặc "user"
            text: Nội dung message
            message_type: Loại message (default: "text")
            
        Returns:
            Message: Message đã tạo
            
        Raises:
            ValueError: Nếu conservation không tồn tại hoặc data không hợp lệ
        """
        # Validate
        if not text or not text.strip():
            raise ValueError("Text không được để trống")
        
        if sender not in ["system", "user"]:
            raise ValueError("Sender phải là 'system' hoặc 'user'")
        
        # Kiểm tra conservation tồn tại
        conservation = self.conservation_repo.find_by_id(conversation_id)
        if not conservation:
            raise ValueError(f"Conservation với ID '{conversation_id}' không tồn tại")
        
        # Tạo message
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            text=text.strip(),
            type=message_type,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        created_message = self.repo.create(message)
        
        # Update conservation message count
        self.conservation_repo.increment_message_count(conversation_id)
        
        return created_message
    
    def get_by_conversation(self, conversation_id: str, page: int = 1, page_size: int = 50) -> Dict:
        """
        Lấy tất cả messages của một conversation với pagination
        
        Args:
            conversation_id: ID của conversation
            page: Trang hiện tại
            page_size: Số messages mỗi trang (default 50 vì messages thường nhiều)
            
        Returns:
            Dict: Pagination result
        """
        page = max(1, page)
        page_size = max(1, min(200, page_size))  # Max 200 cho messages
        skip = (page - 1) * page_size
        
        messages = self.repo.find_by_conversation(conversation_id, skip=skip, limit=page_size)
        total = self.repo.count_by_conversation(conversation_id)
        
        return {
            "items": messages,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "conversation_id": conversation_id
        }
    
    def update_message(self, message_id: str, text: Optional[str] = None) -> Optional[Message]:
        """
        Update message text
        
        Args:
            message_id: ID của message
            text: Text mới
            
        Returns:
            Optional[Message]: Message sau khi update
        """
        existing = self.repo.find_by_id(message_id)
        if not existing:
            raise ValueError(f"Message với ID '{message_id}' không tồn tại")
        
        if text:
            if not text.strip():
                raise ValueError("Text không được để trống")
            existing.text = text.strip()
            existing.updated_at = datetime.utcnow()
        
        return self.repo.update(existing)
    
    def delete_message(self, message_id: str, update_count: bool = True) -> bool:
        """
        Xóa message và optionally update conservation message count
        
        Args:
            message_id: ID của message
            update_count: Có update message count không (default: True)
            
        Returns:
            bool: True nếu xóa thành công
        """
        message = self.repo.find_by_id(message_id)
        if not message:
            raise ValueError(f"Message với ID '{message_id}' không tồn tại")
        
        success = self.repo.delete(message_id)
        
        # Update conservation message count nếu cần
        if success and update_count:
            # Decrement count
            try:
                from bson import ObjectId
                obj_id = ObjectId(message.conversation_id)
                self.conservation_repo.collection.update_one(
                    {"_id": obj_id},
                    {
                        "$inc": {"messageCount": -1},
                        "$set": {"updatedAt": datetime.utcnow()}
                    }
                )
            except:
                pass  # Không fail nếu update count lỗi
        
        return success
    
    def close(self):
        """Đóng connections"""
        super().close()
        self.conservation_repo.close()

