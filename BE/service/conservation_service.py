"""
Conservation Service
"""
from typing import Dict, List, Optional
from datetime import datetime
from BE.service.base_service import BaseService
from BE.repository.conservation_repo import ConservationRepository
from BE.repository.message_repo import MessageRepository
from BE.entities.conservation_entity import Conservation


class ConservationService(BaseService[Conservation]):
    """Service cho Conservation với business logic"""
    
    def __init__(self):
        super().__init__(ConservationRepository())
        self.message_repo = MessageRepository()
    
    def create_conservation(self, title: str, goal: str, facts: List[str] = None) -> Conservation:
        """
        Tạo conservation mới
        
        Args:
            title: Tiêu đề conservation
            goal: Mục tiêu
            facts: Danh sách facts (optional)
            
        Returns:
            Conservation: Conservation đã tạo
        """
        if not title or not title.strip():
            raise ValueError("Title không được để trống")
        
        if not goal or not goal.strip():
            raise ValueError("Goal không được để trống")
        
        conservation = Conservation(
            title=title.strip(),
            goal=goal.strip(),
            message_count=0,
            facts=facts or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return self.repo.create(conservation)
    
    def get_recent(self, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy conservations mới nhất"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_recent(skip=skip, limit=page_size)
        total = self.repo.count()
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def search_by_title(self, title: str, page: int = 1, page_size: int = 10) -> Dict:
        """Search conservations theo title"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_title(title, skip=skip, limit=page_size)
        
        # Count bằng query tương tự
        import re
        pattern = re.compile(re.escape(title), re.IGNORECASE)
        total = self.repo.count({"title": pattern})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def update_conservation(self, conservation_id: str, title: Optional[str] = None, 
                           goal: Optional[str] = None) -> Optional[Conservation]:
        """Update conservation"""
        existing = self.repo.find_by_id(conservation_id)
        if not existing:
            raise ValueError(f"Conservation với ID '{conservation_id}' không tồn tại")
        
        if title:
            if not title.strip():
                raise ValueError("Title không được để trống")
            existing.title = title.strip()
        
        if goal:
            if not goal.strip():
                raise ValueError("Goal không được để trống")
            existing.goal = goal.strip()
        
        existing.updated_at = datetime.utcnow()
        
        return self.repo.update(existing)
    
    def add_fact(self, conservation_id: str, fact: str) -> bool:
        """Thêm fact vào conservation"""
        if not fact or not fact.strip():
            raise ValueError("Fact không được để trống")
        
        conservation = self.repo.find_by_id(conservation_id)
        if not conservation:
            raise ValueError(f"Conservation với ID '{conservation_id}' không tồn tại")
        
        return self.repo.add_fact(conservation_id, fact.strip())
    
    def delete_conservation(self, conservation_id: str, delete_messages: bool = True) -> bool:
        """
        Xóa conservation và optionally xóa tất cả messages
        
        Args:
            conservation_id: ID của conservation
            delete_messages: Có xóa messages không (default: True)
            
        Returns:
            bool: True nếu xóa thành công
        """
        conservation = self.repo.find_by_id(conservation_id)
        if not conservation:
            raise ValueError(f"Conservation với ID '{conservation_id}' không tồn tại")
        
        # Xóa messages nếu cần
        if delete_messages:
            self.message_repo.delete_by_conversation(conservation_id)
        
        return self.repo.delete(conservation_id)
    
    def get_with_messages(self, conservation_id: str) -> Optional[Dict]:
        """
        Lấy conservation cùng với messages
        
        Returns:
            Dict: {conservation: {...}, messages: [...]}
        """
        conservation = self.repo.find_by_id(conservation_id)
        if not conservation:
            return None
        
        # Lấy tất cả messages của conservation
        messages = self.message_repo.find_by_conversation(conservation_id, skip=0, limit=1000)
        
        return {
            "conservation": conservation,
            "messages": messages,
            "total_messages": len(messages)
        }
    
    def close(self):
        """Đóng connections"""
        super().close()
        self.message_repo.close()

