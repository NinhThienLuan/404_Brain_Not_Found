"""
CodeReview Controller - API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from BE.service.code_review_service import CodeReviewService
from BE.entities.code_review_entity import CodeReview

router = APIRouter(prefix="/api/code-reviews", tags=["Code Reviews"])
service = CodeReviewService()


# Request/Response Models
class CodeReviewCreateRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: str = Field(..., min_length=1)
    overall_score: float = Field(..., ge=0, le=10)
    user_id: str
    review_type: str = "general"
    issues: List[Dict] = []
    summary: Optional[str] = None
    improvements: List[str] = []
    additional_notes: Optional[str] = None
    model: str = "gemini-1.5-flash"


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_code_review(data: CodeReviewCreateRequest):
    try:
        entity = CodeReview(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_code_review(id: str):
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Code review not found")
    return entity.to_response()


@router.get("/")
async def get_code_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[str] = None,
    language: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None
):
    try:
        if user_id:
            result = service.get_by_user(user_id, page, page_size)
        elif language:
            result = service.get_by_language(language, page, page_size)
        elif min_score is not None and max_score is not None:
            result = service.get_by_score_range(min_score, max_score, page, page_size)
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
async def delete_code_review(id: str):
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Code review not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

