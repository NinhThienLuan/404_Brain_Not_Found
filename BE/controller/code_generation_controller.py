"""
CodeGeneration Controller - API endpoints
Khớp với structure thực tế trong MongoDB
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from BE.service.code_generation_service import CodeGenerationService
from BE.entities.code_generation_entity import CodeGeneration

router = APIRouter(prefix="/api/code-generations", tags=["Code Generations"])
service = CodeGenerationService()


# Request/Response Models
class CodeGenerationCreateRequest(BaseModel):
    request_id: str = Field(..., description="ID của request")
    files_json: List[Dict] = Field(default_factory=list, description="Array of generated files")
    run_instructions: Optional[str] = Field(None, description="Instructions để chạy code")
    status: str = Field("pending", description="Status: pending, success, error")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_code_generation(data: CodeGenerationCreateRequest):
    """Tạo code generation mới"""
    try:
        entity = CodeGeneration(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_code_generation(id: str):
    """Lấy code generation theo ID"""
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Code generation not found")
    return entity.to_response()


@router.get("/")
async def get_code_generations(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    request_id: Optional[str] = Query(None, description="Filter by request_id"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status")
):
    """Lấy danh sách code generations"""
    try:
        filter_query = {}
        if request_id:
            filter_query["request_id"] = request_id
        if status_filter:
            filter_query["status"] = status_filter
        
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
async def delete_code_generation(id: str):
    """Xóa code generation"""
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Code generation not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
