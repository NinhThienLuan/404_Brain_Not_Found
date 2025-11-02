"""
ExecutionLog Controller - API endpoints
Khớp với structure thực tế trong MongoDB
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, Dict
from BE.service.execution_log_service import ExecutionLogService
from BE.entities.execution_log_entity import ExecutionLog

router = APIRouter(prefix="/api/execution-logs", tags=["Execution Logs"])
service = ExecutionLogService()


# Request/Response Models
class ExecutionLogCreateRequest(BaseModel):
    gen_id: str = Field(..., description="ID của code generation")
    compile_result: Dict = Field(..., description="Kết quả compile")
    test_result: Dict = Field(..., description="Kết quả test")
    lint_result: Dict = Field(..., description="Kết quả lint")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_execution_log(data: ExecutionLogCreateRequest):
    """Tạo execution log mới"""
    try:
        entity = ExecutionLog(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_execution_log(id: str):
    """Lấy execution log theo ID"""
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Execution log not found")
    return entity.to_response()


@router.get("/")
async def get_execution_logs(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    gen_id: Optional[str] = Query(None, description="Filter by gen_id")
):
    """Lấy danh sách execution logs"""
    try:
        filter_query = {}
        if gen_id:
            filter_query["gen_id"] = gen_id
        
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
async def delete_execution_log(id: str):
    """Xóa execution log"""
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Execution log not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
