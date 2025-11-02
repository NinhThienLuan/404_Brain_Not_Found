"""
Context Repository - CRUD operations cho Context collection
"""
from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
from BE.entities.context_entity import Context

load_dotenv()


class ContextRepository:
    """Repository để thao tác với Context collection trong MongoDB"""
    
    def __init__(self):
        """Khởi tạo connection tới MongoDB"""
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
        self.collection: Collection = self.db["contexts"]
    
    def create(self, context: Context) -> Context:
        """Lưu context mới"""
        context_data = context.to_dict(include_id=False)
        result = self.collection.insert_one(context_data)
        context.id = str(result.inserted_id)
        return context
    
    def find_by_session_id(self, session_id: str) -> Optional[Context]:
        """Tìm context theo session_id (lấy context mới nhất)"""
        try:
            data = self.collection.find_one(
                {"session_id": session_id},
                sort=[("created_at", -1)]
            )
            return Context.from_dict(data) if data else None
        except PyMongoError:
            return None
    
    def find_all_by_session(self, session_id: str) -> List[Context]:
        """Lấy tất cả contexts của một session"""
        try:
            cursor = self.collection.find({"session_id": session_id}).sort("created_at", -1)
            return [Context.from_dict(data) for data in cursor]
        except PyMongoError:
            return []
    
    def close(self):
        """Đóng connection"""
        if self.client:
            self.client.close()

