"""
Request Controller - API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, Dict
from BE.service.request_service import RequestService
from BE.entities.request_entity import Request

router = APIRouter(prefix="/api/requests", tags=["Requests"])
service = RequestService()


# Request/Response Models
class RequestCreateRequest(BaseModel):
    request_type: str = Field(..., min_length=1)
    user_id: str
    status: str = "pending"
    data: Optional[Dict] = None
    result_id: Optional[str] = None
    error_message: Optional[str] = None


class RequestUpdateRequest(BaseModel):
    status: Optional[str] = None
    result_id: Optional[str] = None
    error_message: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_request(data: RequestCreateRequest):
    try:
        entity = Request(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_request(id: str):
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Request not found")
    return entity.to_response()


@router.get("/")
async def get_requests(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = None,
    request_type: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status")
):
    try:
        if user_id and request_type:
            # Custom query for user + type
            filter_query = {"user_id": user_id, "request_type": request_type}
            result = service.get_all(page, page_size, filter_query)
        elif user_id:
            result = service.get_by_user(user_id, page, page_size)
        elif request_type:
            result = service.get_by_type(request_type, page, page_size)
        elif status_filter:
            result = service.get_by_status(status_filter, page, page_size)
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
async def update_request(id: str, data: RequestUpdateRequest):
    try:
        existing = service.get_by_id(id)
        if not existing:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Update fields
        if data.status:
            existing.status = data.status
        if data.result_id:
            existing.result_id = data.result_id
        if data.error_message is not None:
            existing.error_message = data.error_message
        
        updated = service.update(existing)
        return updated.to_response()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
async def delete_request(id: str):
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Request not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

