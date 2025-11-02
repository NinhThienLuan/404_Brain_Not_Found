"""
Base Service - Reusable service logic
"""
from typing import List, Optional, Dict, TypeVar, Generic, Type
from BE.repository.base_repo import BaseRepository

T = TypeVar('T')


class BaseService(Generic[T]):
    """Base service với common operations"""
    
    def __init__(self, repository: BaseRepository[T]):
        self.repo = repository
    
    def create(self, entity: T) -> T:
        """Tạo entity mới"""
        return self.repo.create(entity)
    
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Lấy entity theo ID"""
        return self.repo.find_by_id(entity_id)
    
    def get_all(self, page: int = 1, page_size: int = 10, filter_query: dict = None) -> Dict:
        """Lấy danh sách entities với pagination"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        entities = self.repo.find_all(skip=skip, limit=page_size, filter_query=filter_query)
        total = self.repo.count(filter_query)
        
        return {
            "items": entities,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def get_by_user(self, user_id: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy entities của user"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        entities = self.repo.find_by_user(user_id, skip=skip, limit=page_size)
        total = self.repo.count_by_user(user_id)
        
        return {
            "items": entities,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def update(self, entity: T) -> Optional[T]:
        """Update entity"""
        if not entity.id:
            raise ValueError("Entity ID is required for update")
        
        existing = self.repo.find_by_id(entity.id)
        if not existing:
            raise ValueError(f"Entity với ID '{entity.id}' không tồn tại")
        
        return self.repo.update(entity)
    
    def delete(self, entity_id: str) -> bool:
        """Xóa entity"""
        existing = self.repo.find_by_id(entity_id)
        if not existing:
            raise ValueError(f"Entity với ID '{entity_id}' không tồn tại")
        
        return self.repo.delete(entity_id)
    
    def close(self):
        """Đóng connection"""
        self.repo.close()

