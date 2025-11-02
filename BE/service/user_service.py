"""
User Service - Business logic cho User
"""
from typing import List, Optional, Dict
from BE.repository.user_repo import UserRepository
from BE.entities.user_entity import User


class UserService:
    """Service layer xử lý business logic cho User"""
    
    def __init__(self):
        self.repo = UserRepository()
    
    def create_user(self, name: str, email: str) -> User:
        """
        Tạo user mới
        
        Args:
            name: Tên user
            email: Email user
            
        Returns:
            User: User entity vừa tạo
            
        Raises:
            ValueError: Nếu email đã tồn tại hoặc dữ liệu không hợp lệ
        """
        # Validate
        if not name or not name.strip():
            raise ValueError("Tên user không được để trống")
        if not email or not email.strip():
            raise ValueError("Email không được để trống")
        
        # Validate email không trùng
        if self.repo.exists_by_email(email):
            raise ValueError(f"Email '{email}' đã tồn tại trong hệ thống")
        
        # Tạo user entity và save
        user = User(name=name.strip(), email=email.strip())
        return self.repo.create(user)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Lấy thông tin user theo ID
        
        Args:
            user_id: ID của user
            
        Returns:
            Optional[User]: User entity nếu tìm thấy, None nếu không
        """
        return self.repo.find_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Lấy thông tin user theo email
        
        Args:
            email: Email của user
            
        Returns:
            Optional[User]: User entity nếu tìm thấy, None nếu không
        """
        return self.repo.find_by_email(email)
    
    def get_all_users(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Lấy danh sách users với pagination
        
        Args:
            page: Trang hiện tại (bắt đầu từ 1)
            page_size: Số lượng items mỗi trang
            
        Returns:
            Dict: {
                "users": [User, ...],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10
            }
        """
        # Validate và normalize
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        
        skip = (page - 1) * page_size
        
        # Lấy data
        users = self.repo.find_all(skip=skip, limit=page_size)
        total = self.repo.count()
        
        return {
            "users": users,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def update_user(self, user_id: str, name: Optional[str] = None, 
                    email: Optional[str] = None) -> Optional[User]:
        """
        Update thông tin user
        
        Args:
            user_id: ID của user
            name: Tên mới (optional)
            email: Email mới (optional)
            
        Returns:
            Optional[User]: User entity sau khi update, None nếu không tìm thấy
            
        Raises:
            ValueError: Nếu user không tồn tại hoặc email bị trùng
        """
        # Kiểm tra user tồn tại
        existing_user = self.repo.find_by_id(user_id)
        if not existing_user:
            raise ValueError(f"User với ID '{user_id}' không tồn tại")
        
        # Validate dữ liệu mới
        updated_name = name.strip() if name else existing_user.name
        updated_email = email.strip() if email else existing_user.email
        
        if not updated_name:
            raise ValueError("Tên user không được để trống")
        if not updated_email:
            raise ValueError("Email không được để trống")
        
        # Validate email không trùng (nếu thay đổi)
        if updated_email != existing_user.email:
            if self.repo.exists_by_email(updated_email, exclude_id=user_id):
                raise ValueError(f"Email '{updated_email}' đã tồn tại trong hệ thống")
        
        # Tạo user entity với data mới
        updated_user = User(
            id=user_id,
            name=updated_name,
            email=updated_email,
            created_at=existing_user.created_at
        )
        
        return self.repo.update(updated_user)
    
    def delete_user(self, user_id: str) -> bool:
        """
        Xóa user
        
        Args:
            user_id: ID của user
            
        Returns:
            bool: True nếu xóa thành công
            
        Raises:
            ValueError: Nếu user không tồn tại
        """
        # Kiểm tra user tồn tại
        existing_user = self.repo.find_by_id(user_id)
        if not existing_user:
            raise ValueError(f"User với ID '{user_id}' không tồn tại")
        
        return self.repo.delete(user_id)
    
    def close(self):
        """Đóng connection"""
        self.repo.close()

