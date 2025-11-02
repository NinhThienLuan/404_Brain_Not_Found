"""
Base Repository - Reusable MongoDB operations
"""
from typing import List, Optional, Type, TypeVar, Generic
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository với common CRUD operations"""
    
    def __init__(self, collection_name: str, entity_class: Type[T]):
        """
        Khởi tạo base repository
        
        Args:
            collection_name: Tên collection trong MongoDB
            entity_class: Class của entity (để convert dict -> entity)
        """
        self.entity_class = entity_class
        
        # MongoDB connection
        username = os.getenv("MONGO_USERNAME", "mongo")
        password = os.getenv("MONGO_PASSWORD", "OtfagZQFKuslkxmpTCZTlvctRGsQBLnk")
        host = os.getenv("MONGO_HOST", "shortline.proxy.rlwy.net")
        port = int(os.getenv("MONGO_PORT", "21101"))
        database = os.getenv("MONGO_DATABASE", "basic-hackathon")
        
        from urllib.parse import quote_plus
        password_encoded = quote_plus(password)
        uri = f"mongodb://{username}:{password_encoded}@{host}:{port}/{database}?authSource=admin&directConnection=true"
        
        self.client = MongoClient(
            uri,
            directConnection=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        self.db = self.client[database]
        self.collection: Collection = self.db[collection_name]
    
    def create(self, entity: T) -> T:
        """Tạo entity mới"""
        try:
            entity_data = entity.to_dict(include_id=False)
            result = self.collection.insert_one(entity_data)
            entity.id = str(result.inserted_id)
            return entity
        except PyMongoError as e:
            raise Exception(f"Error creating entity: {str(e)}")
    
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """Tìm entity theo ID"""
        try:
            object_id = ObjectId(entity_id)
            data = self.collection.find_one({"_id": object_id})
            return self.entity_class.from_dict(data) if data else None
        except (PyMongoError, ValueError):
            return None
    
    def find_all(self, skip: int = 0, limit: int = 100, filter_query: dict = None) -> List[T]:
        """Lấy danh sách entities"""
        try:
            query = filter_query or {}
            cursor = self.collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
            return [self.entity_class.from_dict(data) for data in cursor]
        except PyMongoError:
            return []
    
    def find_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[T]:
        """Tìm entities theo user_id"""
        return self.find_all(skip=skip, limit=limit, filter_query={"user_id": user_id})
    
    def update(self, entity: T) -> Optional[T]:
        """Update entity"""
        if not entity.id:
            return None
        
        try:
            object_id = ObjectId(entity.id)
            entity_data = entity.to_dict(include_id=False)
            
            result = self.collection.find_one_and_update(
                {"_id": object_id},
                {"$set": entity_data},
                return_document=True
            )
            
            return self.entity_class.from_dict(result) if result else None
        except (PyMongoError, ValueError):
            return None
    
    def delete(self, entity_id: str) -> bool:
        """Xóa entity"""
        try:
            object_id = ObjectId(entity_id)
            result = self.collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except (PyMongoError, ValueError):
            return False
    
    def count(self, filter_query: dict = None) -> int:
        """Đếm số lượng entities"""
        try:
            query = filter_query or {}
            return self.collection.count_documents(query)
        except PyMongoError:
            return 0
    
    def count_by_user(self, user_id: str) -> int:
        """Đếm entities của user"""
        return self.count({"user_id": user_id})
    
    def close(self):
        """Đóng connection"""
        if self.client:
            self.client.close()

