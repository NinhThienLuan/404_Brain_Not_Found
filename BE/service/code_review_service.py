"""
CodeReview Service
"""
from typing import Dict
from BE.service.base_service import BaseService
from BE.repository.code_review_repo import CodeReviewRepository
from BE.entities.code_review_entity import CodeReview


class CodeReviewService(BaseService[CodeReview]):
    """Service cho CodeReview"""
    
    def __init__(self):
        super().__init__(CodeReviewRepository())
    
    def get_by_gen_id(self, gen_id: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code reviews theo gen_id"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_gen_id(gen_id, skip=skip, limit=page_size)
        total = self.repo.count({"gen_id": gen_id})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def get_by_score_range(self, min_score: float, max_score: float, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code reviews theo khoảng điểm"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_score_range(min_score, max_score, skip=skip, limit=page_size)
        total = self.repo.count({"score": {"$gte": min_score, "$lte": max_score}})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
