"""
CodeGeneration Controller - API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from BE.service.code_generation_service import CodeGenerationService
from BE.entities.code_generation_entity import CodeGeneration

router = APIRouter(prefix="/api/code-generations", tags=["Code Generations"])
service = CodeGenerationService()


# Request/Response Models
class CodeGenerationCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    language: str = Field(..., min_length=1)
    generated_code: str
    user_id: str
    framework: Optional[str] = None
    additional_context: Optional[str] = None
    explanation: Optional[str] = None
    model: str = "gemini-2.5-flash"


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_code_generation(data: CodeGenerationCreateRequest):
    try:
        entity = CodeGeneration(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_code_generation(id: str):
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Code generation not found")
    return entity.to_response()


@router.get("/")
async def get_code_generations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = None,
    language: Optional[str] = None
):
    try:
        if user_id:
            result = service.get_by_user(user_id, page, page_size)
        elif language:
            result = service.get_by_language(language, page, page_size)
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
async def delete_code_generation(id: str):
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Code generation not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

