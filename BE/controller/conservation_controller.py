"""
Conservation Controller - API endpoints
Collection name: "conservations" (không phải "conversations")
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, List
from BE.service.conservation_service import ConservationService
from BE.entities.conservation_entity import Conservation

router = APIRouter(prefix="/api/conservations", tags=["Conservations"])
service = ConservationService()


# Request/Response Models
class ConservationCreateRequest(BaseModel):
    """Request để tạo conservation mới"""
    title: str = Field(..., min_length=1, description="Tiêu đề conservation")
    goal: str = Field(..., min_length=1, description="Mục tiêu/goal")
    facts: List[str] = Field(default_factory=list, description="Danh sách facts")


class ConservationUpdateRequest(BaseModel):
    """Request để update conservation"""
    title: Optional[str] = Field(None, min_length=1, description="Tiêu đề mới")
    goal: Optional[str] = Field(None, min_length=1, description="Goal mới")


class AddFactRequest(BaseModel):
    """Request để thêm fact"""
    fact: str = Field(..., min_length=1, description="Fact cần thêm")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_conservation(data: ConservationCreateRequest):
    """
    Tạo conservation mới
    
    - Message count khởi tạo = 0
    - Facts có thể empty
    """
    try:
        conservation = service.create_conservation(
            title=data.title,
            goal=data.goal,
            facts=data.facts
        )
        return conservation.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@router.get("/{id}")
async def get_conservation(id: str):
    """Lấy conservation theo ID"""
    conservation = service.get_by_id(id)
    if not conservation:
        raise HTTPException(status_code=404, detail="Conservation không tồn tại")
    return conservation.to_response()


@router.get("/{id}/with-messages")
async def get_conservation_with_messages(id: str):
    """
    Lấy conservation cùng với tất cả messages
    
    Returns:
    - conservation: Conservation object
    - messages: Array of messages
    - total_messages: Count
    """
    result = service.get_with_messages(id)
    if not result:
        raise HTTPException(status_code=404, detail="Conservation không tồn tại")
    
    return {
        "conservation": result["conservation"].to_response(),
        "messages": [msg.to_response() for msg in result["messages"]],
        "totalMessages": result["total_messages"]
    }


@router.get("/")
async def get_conservations(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    title: Optional[str] = Query(None, description="Search by title"),
    recent: bool = Query(False, description="Lấy recent conservations")
):
    """
    Lấy danh sách conservations
    
    - Support search by title (partial match)
    - Support recent conservations (sorted by createdAt)
    """
    try:
        if title:
            result = service.search_by_title(title, page, page_size)
        elif recent:
            result = service.get_recent(page, page_size)
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
async def update_conservation(id: str, data: ConservationUpdateRequest):
    """Update conservation title hoặc goal"""
    try:
        updated = service.update_conservation(id, title=data.title, goal=data.goal)
        if not updated:
            raise HTTPException(status_code=404, detail="Conservation không tồn tại")
        return updated.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id}/facts")
async def add_fact(id: str, data: AddFactRequest):
    """
    Thêm fact vào conservation
    
    - Fact được thêm vào array facts
    - Updated_at được update tự động
    """
    try:
        success = service.add_fact(id, data.fact)
        if not success:
            raise HTTPException(status_code=404, detail="Conservation không tồn tại")
        
        # Return updated conservation
        conservation = service.get_by_id(id)
        return conservation.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
async def delete_conservation(
    id: str,
    delete_messages: bool = Query(True, description="Có xóa messages không")
):
    """
    Xóa conservation
    
    - Optionally xóa tất cả messages trong conservation
    - Default: xóa cả messages
    """
    try:
        success = service.delete_conservation(id, delete_messages=delete_messages)
        if not success:
            raise HTTPException(status_code=404, detail="Conservation không tồn tại")
        
        msg = "Conservation và messages đã được xóa" if delete_messages else "Conservation đã được xóa"
        return {"message": msg}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# NESTED ENDPOINTS - Messages trong Conservation
# Dùng cho Chatbox UI (tiện hơn)
# ============================================================

class MessageInConservationRequest(BaseModel):
    """Request để thêm message vào conservation (nested endpoint)"""
    sender: str = Field(..., description="Sender: 'system' hoặc 'user'")
    text: str = Field(..., min_length=1, description="Nội dung message")
    type: str = Field("text", description="Loại message")


@router.post("/{conservation_id}/messages", status_code=status.HTTP_201_CREATED)
async def add_message_to_conservation(conservation_id: str, data: MessageInConservationRequest):
    """
    Thêm message vào conservation (Nested endpoint cho Chatbox)
    
    - Tự động link message với conservation
    - Auto update conservation message count
    - Dùng cho UI chatbox khi user send message
    
    Example:
    ```
    POST /api/conservations/6905a4bada4db5565a169084/messages
    {
      "sender": "user",
      "text": "Hello!"
    }
    ```
    """
    try:
        # Import message service
        from BE.service.message_service import MessageService
        message_service = MessageService()
        
        # Tạo message với conservation_id từ URL
        message = message_service.create_message(
            conversation_id=conservation_id,
            sender=data.sender,
            text=data.text,
            message_type=data.type
        )
        
        return message.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@router.delete("/{conservation_id}/messages/{message_id}")
async def remove_message_from_conservation(
    conservation_id: str,
    message_id: str,
    update_count: bool = Query(True, description="Update message count")
):
    """
    Xóa message từ conservation (Nested endpoint cho Chatbox)
    
    - Verify message thuộc về conservation
    - Auto update conservation message count
    - Dùng cho UI chatbox khi user xóa message
    
    Example:
    ```
    DELETE /api/conservations/6905a4bada4db5565a169084/messages/6905a37f9d893e353a0c5fc2
    ```
    """
    try:
        # Import message service
        from BE.service.message_service import MessageService
        message_service = MessageService()
        
        # Verify message exists và thuộc về conservation này
        message = message_service.get_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message không tồn tại")
        
        if message.conversation_id != conservation_id:
            raise HTTPException(
                status_code=400,
                detail=f"Message không thuộc về conservation này"
            )
        
        # Xóa message
        success = message_service.delete_message(message_id, update_count=update_count)
        if not success:
            raise HTTPException(status_code=500, detail="Không thể xóa message")
        
        return {"message": "Message đã được xóa khỏi conservation"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

