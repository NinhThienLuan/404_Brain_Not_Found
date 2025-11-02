"""
CodeReview Repository
"""
from typing import List
from BE.repository.base_repo import BaseRepository
from BE.entities.code_review_entity import CodeReview


class CodeReviewRepository(BaseRepository[CodeReview]):
    """Repository cho CodeReview collection"""
    
    def __init__(self):
        super().__init__("code_reviews", CodeReview)
    
    def find_by_gen_id(self, gen_id: str, skip: int = 0, limit: int = 100) -> List[CodeReview]:
        """Tìm code reviews theo gen_id"""
        return self.find_all(skip=skip, limit=limit, filter_query={"gen_id": gen_id})
    
    def find_by_score_range(self, min_score: float, max_score: float, skip: int = 0, limit: int = 100) -> List[CodeReview]:
        """Tìm code reviews theo khoảng điểm"""
        return self.find_all(
            skip=skip,
            limit=limit,
            filter_query={"score": {"$gte": min_score, "$lte": max_score}}
        )
