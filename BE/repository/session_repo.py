"""
Session Repository - CRUD operations cho Session collection
"""
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
from BE.entities.session_entity import Session, WorkflowStep

load_dotenv()


class SessionRepository:
    """Repository để thao tác với Session collection trong MongoDB"""
    
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
        self.collection: Collection = self.db["sessions"]
    
    def create(self, session: Session) -> Session:
        """Tạo session mới"""
        # Ensure timestamps are set
        if not session.created_at:
            session.created_at = datetime.utcnow()
        if not session.updated_at:
            session.updated_at = datetime.utcnow()
        
        session_data = session.to_dict(include_id=False)
        result = self.collection.insert_one(session_data)
        session.id = str(result.inserted_id)
        return session
    
    def find_by_id(self, session_id: str) -> Optional[Session]:
        """Tìm session theo ID"""
        try:
            object_id = ObjectId(session_id)
            data = self.collection.find_one({"_id": object_id})
            return Session.from_dict(data) if data else None
        except (PyMongoError, ValueError):
            return None
    
    def find_by_user_id(self, user_id: str, limit: int = 10) -> List[Session]:
        """Lấy danh sách sessions của user"""
        try:
            cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
            return [Session.from_dict(data) for data in cursor]
        except PyMongoError:
            return []
    
    def update(self, session: Session) -> Optional[Session]:
        """Update session"""
        if not session.id:
            return None
        
        try:
            object_id = ObjectId(session.id)
            update_data = session.to_dict(include_id=False)
            
            result = self.collection.find_one_and_update(
                {"_id": object_id},
                {"$set": update_data},
                return_document=True
            )
            
            return Session.from_dict(result) if result else None
        except (PyMongoError, ValueError):
            return None
    
    def delete(self, session_id: str) -> bool:
        """Xóa session"""
        try:
            object_id = ObjectId(session_id)
            result = self.collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except (PyMongoError, ValueError):
            return False
    
    def update_step(self, session_id: str, new_step: WorkflowStep) -> bool:
        """Cập nhật step của session"""
        try:
            object_id = ObjectId(session_id)
            result = self.collection.update_one(
                {"_id": object_id},
                {"$set": {
                    "current_step": new_step.value,
                    "updated_at": datetime.utcnow()
                }}
            )
            return result.modified_count > 0
        except (PyMongoError, ValueError):
            return False
    
    def add_code_history(self, session_id: str, code_entry: dict) -> bool:
        """Thêm code vào history"""
        try:
            object_id = ObjectId(session_id)
            result = self.collection.update_one(
                {"_id": object_id},
                {
                    "$push": {"code_history": code_entry},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except (PyMongoError, ValueError):
            return False
    
    def close(self):
        """Đóng connection"""
        if self.client:
            self.client.close()

