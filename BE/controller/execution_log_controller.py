"""
ExecutionLog Controller - API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from BE.service.execution_log_service import ExecutionLogService
from BE.entities.execution_log_entity import ExecutionLog

router = APIRouter(prefix="/api/execution-logs", tags=["Execution Logs"])
service = ExecutionLogService()


# Request/Response Models
class ExecutionLogCreateRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: str = Field(..., min_length=1)
    user_id: str
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    status: str = "pending"
    code_generation_id: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_execution_log(data: ExecutionLogCreateRequest):
    try:
        entity = ExecutionLog(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_execution_log(id: str):
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Execution log not found")
    return entity.to_response()


@router.get("/")
async def get_execution_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status")
):
    try:
        if user_id:
            result = service.get_by_user(user_id, page, page_size)
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


@router.delete("/{id}")
async def delete_execution_log(id: str):
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Execution log not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

