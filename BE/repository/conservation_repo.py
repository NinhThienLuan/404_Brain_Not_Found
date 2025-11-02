"""
Conservation Repository
Lưu ý: Collection name là "conservations" (không phải "conversations")
"""
from typing import List, Optional
from pymongo.errors import PyMongoError
from BE.repository.base_repo import BaseRepository
from BE.entities.conservation_entity import Conservation


class ConservationRepository(BaseRepository[Conservation]):
    """Repository cho Conservations collection"""
    
    def __init__(self):
        # Collection name chính xác trong MongoDB là "conservations"
        super().__init__("conservations", Conservation)
    
    def find_by_title(self, title: str, skip: int = 0, limit: int = 100) -> List[Conservation]:
        """Tìm conservations theo title (partial match)"""
        try:
            import re
            pattern = re.compile(re.escape(title), re.IGNORECASE)
            return self.find_all(
                skip=skip,
                limit=limit,
                filter_query={"title": pattern}
            )
        except:
            return []
    
    def find_recent(self, skip: int = 0, limit: int = 10) -> List[Conservation]:
        """Lấy các conservations mới nhất"""
        try:
            cursor = self.collection.find().sort("createdAt", -1).skip(skip).limit(limit)
            return [Conservation.from_dict(data) for data in cursor]
        except PyMongoError:
            return []
    
    def increment_message_count(self, conservation_id: str) -> bool:
        """
        Tăng message count khi có message mới
        
        Args:
            conservation_id: ID của conservation
            
        Returns:
            bool: True nếu thành công
        """
        try:
            from bson import ObjectId
            obj_id = ObjectId(conservation_id)
            result = self.collection.update_one(
                {"_id": obj_id},
                {
                    "$inc": {"messageCount": 1},
                    "$set": {"updatedAt": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except:
            return False
    
    def add_fact(self, conservation_id: str, fact: str) -> bool:
        """
        Thêm fact vào conservation
        
        Args:
            conservation_id: ID của conservation
            fact: Fact cần thêm
            
        Returns:
            bool: True nếu thành công
        """
        try:
            from bson import ObjectId
            obj_id = ObjectId(conservation_id)
            result = self.collection.update_one(
                {"_id": obj_id},
                {
                    "$push": {"facts": fact},
                    "$set": {"updatedAt": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except:
            return False

