"""
CodeReview Controller - API endpoints
Khớp với structure thực tế trong MongoDB
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from BE.service.code_review_service import CodeReviewService
from BE.entities.code_review_entity import CodeReview

router = APIRouter(prefix="/api/code-reviews", tags=["Code Reviews"])
service = CodeReviewService()


# Request/Response Models
class CodeReviewCreateRequest(BaseModel):
    gen_id: str = Field(..., description="ID của code generation")
    review_markdown: str = Field(..., description="Review content in markdown")
    score: int = Field(..., ge=0, le=10, description="Score từ 0-10")
    summary: Optional[str] = Field(None, description="Summary của review")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_code_review(data: CodeReviewCreateRequest):
    """Tạo code review mới"""
    try:
        entity = CodeReview(**data.dict())
        created = service.create(entity)
        return created.to_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
async def get_code_review(id: str):
    """Lấy code review theo ID"""
    entity = service.get_by_id(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Code review not found")
    return entity.to_response()


@router.get("/")
async def get_code_reviews(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    gen_id: Optional[str] = Query(None, description="Filter by gen_id"),
    min_score: Optional[int] = Query(None, ge=0, le=10, description="Minimum score"),
    max_score: Optional[int] = Query(None, ge=0, le=10, description="Maximum score")
):
    """Lấy danh sách code reviews"""
    try:
        filter_query = {}
        if gen_id:
            filter_query["gen_id"] = gen_id
        if min_score is not None and max_score is not None:
            result = service.get_by_score_range(float(min_score), float(max_score), page, page_size)
        elif filter_query:
            result = service.get_all(page, page_size, filter_query)
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
    """Xóa code review"""
    try:
        success = service.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Code review not found")
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
