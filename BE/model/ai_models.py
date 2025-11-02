from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CodeGenerationRequest(BaseModel):
    """Request model for code generation"""
    prompt: str = Field(..., description="The prompt describing what code to generate")
    language: str = Field(default="python", description="Programming language")
    framework: Optional[str] = Field(default=None, description="Framework to use")
    additional_context: Optional[str] = Field(default=None, description="Additional context or requirements")
    model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model to use: gemini-2.5-flash, gemini-1.5-pro, gemini-1.5-flash"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt": "Create a function to calculate fibonacci sequence",
                "language": "python",
                "framework": "fastapi",
                "additional_context": "Use recursion with memoization",
                "model": "gemini-2.5-flash"
            }
        }
    }


class CodeGenerationResponse(BaseModel):
    """Response model for code generation"""
    generated_code: str
    explanation: str
    language: str
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None


class CodeReviewRequest(BaseModel):
    """Request model for code review"""
    code: str = Field(..., description="The code to review")
    language: str = Field(..., description="Programming language of the code")
    review_type: str = Field(default="general", description="Type of review: general, security, performance, style")
    additional_notes: Optional[str] = Field(default=None, description="Additional notes for the review")
    model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model to use: gemini-2.5-flash, gemini-1.5-pro, gemini-1.5-flash"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "code": "def fibonacci(n):\n    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
                "language": "python",
                "review_type": "performance",
                "additional_notes": "Focus on optimization",
                "model": "gemini-2.5-flash"
            }
        }
    }


class ReviewIssue(BaseModel):
    """Model for a single review issue"""
    severity: str = Field(..., description="Severity: critical, high, medium, low, info")
    line_number: Optional[int] = Field(default=None, description="Line number where issue occurs")
    issue_type: str = Field(..., description="Type: bug, style, performance, security, best-practice")
    description: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggested fix or improvement")


class CodeReviewResponse(BaseModel):
    """Response model for code review"""
    overall_score: float = Field(..., ge=0, le=10, description="Overall code quality score (0-10)")
    issues: List[ReviewIssue] = Field(default_factory=list)
    summary: str
    improvements: List[str] = Field(default_factory=list)
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None
