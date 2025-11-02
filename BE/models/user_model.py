"""
User Model - Định nghĩa schema cho User trong MongoDB
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type để serialize với Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    """Model cho User trong database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    created_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


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
    created_at: str

    class Config:
        allow_population_by_field_name = True

