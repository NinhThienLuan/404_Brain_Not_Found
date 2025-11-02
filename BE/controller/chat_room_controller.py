"""
ChatRoom Controller - API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from BE.service.chat_room_service import ChatRoomService
from BE.entities.chat_room_entity import ChatRoom

router = APIRouter(prefix="/api/chat-rooms", tags=["Chat Rooms"])
service = ChatRoomService()


# Request/Response Models
class ChatRoomCreateRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    is_active: bool = True


class ChatRoomUpdateRequest(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat_room(data: ChatRoomCreateRequest):
    try:
        entity = ChatRoom(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_chat_room(id: str):
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return entity.to_response()


@router.get("/")
async def get_chat_rooms(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = None,
    active_only: bool = Query(False)
):
    try:
        if user_id:
            result = service.get_by_user(user_id, page, page_size)
        elif active_only:
            result = service.get_active(page, page_size)
        else:
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


@router.put("/{id}")
async def update_chat_room(id: str, data: ChatRoomUpdateRequest):
    try:
        existing = service.get_by_id(id)
        if not existing:
            raise HTTPException(status_code=404, detail="Chat room not found")
        
        if data.title:
            existing.title = data.title
        if data.is_active is not None:
            existing.is_active = data.is_active
        
        updated = service.update(existing)
        return updated.to_response()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
async def delete_chat_room(id: str):
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Chat room not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

