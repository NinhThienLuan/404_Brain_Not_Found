"""
Message Controller - API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from BE.service.message_service import MessageService
from BE.entities.message_entity import Message

router = APIRouter(prefix="/api/messages", tags=["Messages"])
service = MessageService()


# Request/Response Models
class MessageCreateRequest(BaseModel):
    """Request để tạo message mới"""
    conversationId: str = Field(..., description="ID của conversation")
    sender: str = Field(..., description="Sender: 'system' hoặc 'user'")
    text: str = Field(..., min_length=1, description="Nội dung message")
    type: str = Field("text", description="Loại message")


class MessageUpdateRequest(BaseModel):
    """Request để update message"""
    text: str = Field(..., min_length=1, description="Text mới")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(data: MessageCreateRequest):
    """
    Tạo message mới
    
    - Tự động update message count của conservation
    - Sender phải là 'system' hoặc 'user'
    """
    try:
        message = service.create_message(
            conversation_id=data.conversationId,
            sender=data.sender,
            text=data.text,
            message_type=data.type
        )
        return message.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@router.get("/{id}")
async def get_message(id: str):
    """Lấy message theo ID"""
    message = service.get_by_id(id)
    if not message:
        raise HTTPException(status_code=404, detail="Message không tồn tại")
    return message.to_response()


@router.get("/")
async def get_messages(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(50, ge=1, le=200, description="Messages per page (max 200)")
):
    """Lấy tất cả messages"""
    try:
        result = service.get_all(page, page_size)
        return {
            "items": [item.to_response() for item in result["items"]],
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "total_pages": result["total_pages"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{conversation_id}")
async def get_messages_by_conversation(
    conversation_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200)
):
    """
    Lấy tất cả messages của một conversation
    
    - Sorted by createdAt (mới nhất trước)
    - Pagination support
    """
    try:
        result = service.get_by_conversation(conversation_id, page, page_size)
        return {
            "items": [item.to_response() for item in result["items"]],
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "total_pages": result["total_pages"],
            "conversationId": result["conversation_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}")
async def update_message(id: str, data: MessageUpdateRequest):
    """Update message text"""
    try:
        updated = service.update_message(id, data.text)
        if not updated:
            raise HTTPException(status_code=404, detail="Message không tồn tại")
        return updated.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
async def delete_message(
    id: str,
    update_count: bool = Query(True, description="Update conservation message count")
):
    """
    Xóa message
    
    - Optionally update conservation message count
    """
    try:
        success = service.delete_message(id, update_count=update_count)
        if not success:
            raise HTTPException(status_code=404, detail="Message không tồn tại")
        return {"message": "Message đã được xóa"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

