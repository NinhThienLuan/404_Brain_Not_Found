"""
Request Controller - API endpoints
Khớp với structure thực tế trong MongoDB
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from BE.service.request_service import RequestService
from BE.entities.request_entity import Request

router = APIRouter(prefix="/api/requests", tags=["Requests"])
service = RequestService()


# Request/Response Models
class RequestCreateRequest(BaseModel):
    user_id: str = Field(..., description="ID của user")
    requirement_text: str = Field(..., min_length=1, description="Yêu cầu của user")
    language: str = Field(..., description="Programming language")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_request(data: RequestCreateRequest):
    """Tạo request mới"""
    try:
        entity = Request(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_request(id: str):
    """Lấy request theo ID"""
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Request not found")
    return entity.to_response()


@router.get("/")
async def get_requests(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    user_id: Optional[str] = Query(None, description="Filter by user_id"),
    language: Optional[str] = Query(None, description="Filter by language")
):
    """Lấy danh sách requests"""
    try:
        filter_query = {}
        if user_id:
            filter_query["user_id"] = user_id
        if language:
            filter_query["language"] = language
        
        result = service.get_all(page, page_size, filter_query if filter_query else None)
        
        return {
            "items": [item.to_response() for item in result["items"]],
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "total_pages": result["total_pages"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
async def delete_request(id: str):
    """Xóa request"""
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Request not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
