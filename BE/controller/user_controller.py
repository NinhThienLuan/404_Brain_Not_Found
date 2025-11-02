"""
User Controller - API endpoints cho User
"""
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from BE.service.user_service import UserService
from BE.entities.user_entity import User
from pydantic import BaseModel, EmailStr, Field


# Request/Response Models
class UserCreateRequest(BaseModel):
    """Request body để tạo user mới"""
    name: str = Field(..., min_length=1, max_length=100, example="Nguyễn Văn A")
    email: EmailStr = Field(..., example="a@example.com")


class UserUpdateRequest(BaseModel):
    """Request body để update user"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    """Response trả về cho client"""
    id: str = Field(..., alias="_id")
    name: str
    email: str
    created_at: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class MessageResponse(BaseModel):
    """Response cho message"""
    message: str


# Router
router = APIRouter(prefix="/api/users", tags=["Users"])
user_service = UserService()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateRequest):
    """
    Tạo user mới
    
    - **name**: Tên user (bắt buộc)
    - **email**: Email user (bắt buộc, phải là email hợp lệ)
    """
    try:
        created_user = user_service.create_user(
            name=user.name,
            email=user.email
        )
        return created_user.to_response()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Lấy thông tin user theo ID
    
    - **user_id**: ID của user (trong URL)
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy user với ID '{user_id}'"
        )
    return user.to_response()


@router.get("/")
async def get_users(
    page: int = Query(1, ge=1, description="Số trang (bắt đầu từ 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Số lượng items mỗi trang")
):
    """
    Lấy danh sách users với pagination
    
    - **page**: Số trang (mặc định 1)
    - **page_size**: Số lượng items mỗi trang (mặc định 10, tối đa 100)
    
    Returns:
    ```json
    {
        "users": [...],
        "total": 100,
        "page": 1,
        "page_size": 10,
        "total_pages": 10
    }
    ```
    """
    try:
        result = user_service.get_all_users(page=page, page_size=page_size)
        # Convert User entities to response dicts
        return {
            "users": [user.to_response() for user in result["users"]],
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "total_pages": result["total_pages"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách users: {str(e)}"
        )


@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    """
    Lấy thông tin user theo email
    
    - **email**: Email của user
    """
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy user với email '{email}'"
        )
    return user.to_response()


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdateRequest):
    """
    Update thông tin user
    
    - **user_id**: ID của user (trong URL)
    - **name**: Tên mới (optional)
    - **email**: Email mới (optional)
    """
    try:
        updated_user = user_service.update_user(
            user_id=user_id,
            name=user.name,
            email=user.email
        )
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy user với ID '{user_id}'"
            )
        return updated_user.to_response()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi update user: {str(e)}"
        )


@router.patch("/{user_id}", response_model=UserResponse)
async def partial_update_user(user_id: str, user: UserUpdateRequest):
    """
    Partial update user (giống PUT nhưng semantic khác)
    
    - **user_id**: ID của user (trong URL)
    - **name**: Tên mới (optional)
    - **email**: Email mới (optional)
    """
    return await update_user(user_id, user)


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: str):
    """
    Xóa user
    
    - **user_id**: ID của user (trong URL)
    """
    try:
        success = user_service.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy user với ID '{user_id}'"
            )
        return {"message": f"Đã xóa user với ID '{user_id}' thành công"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi xóa user: {str(e)}"
        )

