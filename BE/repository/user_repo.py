"""
User Repository - CRUD operations cho User collection
"""
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
from BE.entities.user_entity import User

load_dotenv()


class UserRepository:
    """Repository để thao tác với User collection trong MongoDB"""
    
    def __init__(self):
        """Khởi tạo connection tới MongoDB"""
        username = os.getenv("MONGO_USERNAME", "mongo")
        password = os.getenv("MONGO_PASSWORD", "OtfagZQFKuslkxmpTCZTlvctRGsQBLnk")
        host = os.getenv("MONGO_HOST", "shortline.proxy.rlwy.net")
        port = int(os.getenv("MONGO_PORT", "21101"))
        database = os.getenv("MONGO_DATABASE", "basic-hackathon")
        
        # Encode password
        from urllib.parse import quote_plus
        password_encoded = quote_plus(password)
        
        # Create connection URI
        uri = f"mongodb://{username}:{password_encoded}@{host}:{port}/{database}?authSource=admin&directConnection=true"
        
        # Connect to MongoDB
        self.client = MongoClient(
            uri,
            directConnection=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        self.db = self.client[database]
        self.collection: Collection = self.db["users"]
    
    def create(self, user: User) -> User:
        """
        Tạo user mới trong database
        
        Args:
            user: User entity cần tạo
            
        Returns:
            User: User entity với ID đã được gán
        """
        user_data = user.to_dict(include_id=False)
        result = self.collection.insert_one(user_data)
        
        user.id = str(result.inserted_id)
        return user
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Tìm user theo ID
        
        Args:
            user_id: ID của user (string)
            
        Returns:
            Optional[User]: User entity nếu tìm thấy, None nếu không
        """
        try:
            object_id = ObjectId(user_id)
            data = self.collection.find_one({"_id": object_id})
            return User.from_dict(data) if data else None
        except (PyMongoError, ValueError):
            return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Tìm user theo email
        
        Args:
            email: Email của user
            
        Returns:
            Optional[User]: User entity nếu tìm thấy, None nếu không
        """
        try:
            data = self.collection.find_one({"email": email})
            return User.from_dict(data) if data else None
        except PyMongoError:
            return None
    
    def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lấy danh sách tất cả users với pagination
        
        Args:
            skip: Số lượng record bỏ qua
            limit: Số lượng record tối đa trả về
            
        Returns:
            List[User]: Danh sách User entities
        """
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            return [User.from_dict(data) for data in cursor]
        except PyMongoError:
            return []
    
    def update(self, user: User) -> Optional[User]:
        """
        Update user trong database
        
        Args:
            user: User entity với thông tin đã cập nhật (phải có ID)
            
        Returns:
            Optional[User]: User entity sau khi update, None nếu không tìm thấy
        """
        if not user.id:
            return None
        
        try:
            object_id = ObjectId(user.id)
            
            # Chỉ update name và email (không update created_at và _id)
            update_data = {
                "name": user.name,
                "email": user.email
            }
            
            result = self.collection.find_one_and_update(
                {"_id": object_id},
                {"$set": update_data},
                return_document=True
            )
            
            return User.from_dict(result) if result else None
        except (PyMongoError, ValueError):
            return None
    
    def delete(self, user_id: str) -> bool:
        """
        Xóa user khỏi database
        
        Args:
            user_id: ID của user cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu không
        """
        try:
            object_id = ObjectId(user_id)
            result = self.collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except (PyMongoError, ValueError):
            return False
    
    def count(self, filter_query: dict = None) -> int:
        """
        Đếm số lượng users
        
        Args:
            filter_query: Query để filter (optional)
            
        Returns:
            int: Số lượng users
        """
        try:
            if filter_query is None:
                filter_query = {}
            return self.collection.count_documents(filter_query)
        except PyMongoError:
            return 0
    
    def exists_by_email(self, email: str, exclude_id: str = None) -> bool:
        """
        Kiểm tra xem email đã tồn tại chưa
        
        Args:
            email: Email cần kiểm tra
            exclude_id: ID user cần loại trừ (khi update)
            
        Returns:
            bool: True nếu email đã tồn tại
        """
        try:
            query = {"email": email}
            if exclude_id:
                try:
                    query["_id"] = {"$ne": ObjectId(exclude_id)}
                except ValueError:
                    pass
            
            return self.collection.count_documents(query) > 0
        except PyMongoError:
            return False
    
    def close(self):
        """Đóng connection tới MongoDB"""
        if self.client:
            self.client.close()

