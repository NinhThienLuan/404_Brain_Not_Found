"""
Chat Controller - REST API endpoints cho Chat & ChatRoom
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from BE.service.chat_room_service import ChatRoomService
from BE.service.message_service import MessageService

# Router
router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Services
chat_room_service = ChatRoomService()
message_service = MessageService()


# ==================== Pydantic Models ====================

class CreateRoomRequest(BaseModel):
    """Request để tạo phòng chat mới"""
    user_id: str = Field(..., description="ID của user tạo phòng")
    title: Optional[str] = Field(None, description="Tiêu đề phòng chat")


class UpdateRoomRequest(BaseModel):
    """Request để cập nhật phòng chat"""
    title: str = Field(..., description="Tiêu đề mới")


class SendMessageRequest(BaseModel):
    """Request để gửi tin nhắn"""
    chat_room_id: str = Field(..., description="ID của phòng chat")
    content: str = Field(..., description="Nội dung tin nhắn")
    sender_type: str = Field("user", description="Loại người gửi: user hoặc ai")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Dữ liệu bổ sung")


class RoomResponse(BaseModel):
    """Response cho ChatRoom"""
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


class MessageResponse(BaseModel):
    """Response cho Message"""
    id: str
    chat_room_id: str
    content: str
    sender_type: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class MessageListResponse(BaseModel):
    """Response cho danh sách tin nhắn"""
    messages: List[MessageResponse]
    total: int
    chat_room_id: str


# ==================== ChatRoom Routes ====================

@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_room(request: CreateRoomRequest):
    """
    Tạo phòng chat mới
    
    - **user_id**: ID của user tạo phòng
    - **title**: Tiêu đề phòng (tự động nếu không có)
    """
    try:
        room = chat_room_service.create_room(
            user_id=request.user_id,
            title=request.title
        )
        
        return RoomResponse(
            id=room.id,
            user_id=room.user_id,
            title=room.title,
            created_at=room.created_at,
            updated_at=room.updated_at,
            is_active=room.is_active
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat room: {str(e)}"
        )


@router.get("/rooms/user/{user_id}", response_model=List[RoomResponse])
async def get_user_rooms(
    user_id: str,
    limit: int = Query(50, ge=1, le=100, description="Số lượng phòng tối đa")
):
    """
    Lấy tất cả phòng chat của user
    
    - **user_id**: ID của user
    - **limit**: Số lượng phòng tối đa (mặc định 50)
    """
    try:
        rooms = chat_room_service.get_user_rooms(user_id, limit)
        
        return [
            RoomResponse(
                id=room.id,
                user_id=room.user_id,
                title=room.title,
                created_at=room.created_at,
                updated_at=room.updated_at,
                is_active=room.is_active
            )
            for room in rooms
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user rooms: {str(e)}"
        )


@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room_detail(room_id: str):
    """
    Lấy chi tiết một phòng chat
    
    - **room_id**: ID của phòng chat
    """
    try:
        room = chat_room_service.get_by_id(room_id)
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat room not found: {room_id}"
            )
        
        return RoomResponse(
            id=room.id,
            user_id=room.user_id,
            title=room.title,
            created_at=room.created_at,
            updated_at=room.updated_at,
            is_active=room.is_active
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get room detail: {str(e)}"
        )


@router.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(room_id: str, request: UpdateRoomRequest):
    """
    Cập nhật tiêu đề phòng chat
    
    - **room_id**: ID của phòng chat
    - **title**: Tiêu đề mới
    """
    try:
        room = chat_room_service.update_title(room_id, request.title)
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat room not found: {room_id}"
            )
        
        return RoomResponse(
            id=room.id,
            user_id=room.user_id,
            title=room.title,
            created_at=room.created_at,
            updated_at=room.updated_at,
            is_active=room.is_active
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update room: {str(e)}"
        )


@router.delete("/rooms/{room_id}")
async def delete_room(room_id: str):
    """
    Xóa phòng chat (soft delete)
    
    - **room_id**: ID của phòng chat
    """
    try:
        success = chat_room_service.delete_room(room_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat room not found: {room_id}"
            )
        
        return {
            "message": "Chat room deleted successfully",
            "room_id": room_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete room: {str(e)}"
        )


# ==================== Message Routes ====================

@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(request: SendMessageRequest):
    """
    Gửi tin nhắn mới vào phòng chat
    
    - **chat_room_id**: ID của phòng chat
    - **content**: Nội dung tin nhắn
    - **sender_type**: Loại người gửi (user hoặc ai)
    - **metadata**: Dữ liệu bổ sung (tùy chọn)
    """
    try:
        message = message_service.send_message(
            chat_room_id=request.chat_room_id,
            content=request.content,
            sender_type=request.sender_type,
            metadata=request.metadata
        )
        
        return MessageResponse(
            id=message.id,
            chat_room_id=message.chat_room_id,
            content=message.content,
            sender_type=message.sender_type,
            created_at=message.created_at,
            metadata=message.metadata
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )


@router.get("/messages/room/{chat_room_id}", response_model=MessageListResponse)
async def get_room_messages(
    chat_room_id: str,
    limit: int = Query(100, ge=1, le=500, description="Số lượng tin nhắn tối đa"),
    skip: int = Query(0, ge=0, description="Số lượng tin nhắn bỏ qua")
):
    """
    Lấy tin nhắn trong phòng chat
    
    - **chat_room_id**: ID của phòng chat
    - **limit**: Số lượng tin nhắn tối đa (mặc định 100)
    - **skip**: Số lượng tin nhắn bỏ qua cho pagination (mặc định 0)
    """
    try:
        messages = message_service.get_room_messages(chat_room_id, limit, skip)
        total = message_service.count_messages(chat_room_id)
        
        return MessageListResponse(
            messages=[
                MessageResponse(
                    id=msg.id,
                    chat_room_id=msg.chat_room_id,
                    content=msg.content,
                    sender_type=msg.sender_type,
                    created_at=msg.created_at,
                    metadata=msg.metadata
                )
                for msg in messages
            ],
            total=total,
            chat_room_id=chat_room_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message_detail(message_id: str):
    """
    Lấy chi tiết một tin nhắn
    
    - **message_id**: ID của tin nhắn
    """
    try:
        message = message_service.get_by_id(message_id)
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Message not found: {message_id}"
            )
        
        return MessageResponse(
            id=message.id,
            chat_room_id=message.chat_room_id,
            content=message.content,
            sender_type=message.sender_type,
            created_at=message.created_at,
            metadata=message.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get message detail: {str(e)}"
        )
