from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from BE.model.ai_models import (
    CodeGenerationRequest, 
    CodeGenerationResponse,
    CodeReviewRequest,
    CodeReviewResponse
)
from BE.service.ai_service import CodeGenerationService, CodeReviewService


# Create APIRouter (equivalent to Flask Blueprint)
ai_router = APIRouter(prefix="/ai", tags=["AI"])

# Initialize services
code_gen_service = CodeGenerationService()
code_review_service = CodeReviewService()


@ai_router.post(
    "/generate",
    response_model=CodeGenerationResponse,
    summary="Generate Code",
    description="Generate code based on natural language prompt"
)
async def generate_code(request: CodeGenerationRequest) -> CodeGenerationResponse:
    """
    Generate code using AI based on the provided prompt.
    
    - **prompt**: Description of what code to generate (required)
    - **language**: Programming language (default: python)
    - **framework**: Framework to use (optional)
    - **additional_context**: Extra context or requirements (optional)
    """
    try:
        # Generate code
        response = code_gen_service.generate_code(request)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.error_message or "Code generation failed"
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@ai_router.post(
    "/review",
    response_model=CodeReviewResponse,
    summary="Review Code",
    description="Analyze and review code quality with AI"
)
async def review_code(request: CodeReviewRequest) -> CodeReviewResponse:
    """
    Review code and provide feedback, issues, and suggestions.
    
    - **code**: The code to review (required)
    - **language**: Programming language (required)
    - **review_type**: Type of review - general, security, performance, style (default: general)
    - **additional_notes**: Additional notes for the review (optional)
    """
    try:
        # Review code
        response = code_review_service.review_code(request)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.error_message or "Code review failed"
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@ai_router.get(
    "/health",
    summary="Health Check",
    description="Check if the AI service is running"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Agent API",
        "version": "2.0.0"
    }
