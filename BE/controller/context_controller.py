"""

Context Controller - API cho Context Parsing Service

"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from model.context_models import ContextParsingRequest, ContextParsingResponse
from model.intent_models import ParsedContextV2
from service.context_parsing_service import ContextParsingService

# Create router
context_router = APIRouter(prefix="/context", tags=["Context Parsing"])

# Initialize service
context_service = ContextParsingService()

logger = logging.getLogger(__name__)


@context_router.post("/parse", response_model=ContextParsingResponse)
async def parse_context(request: ContextParsingRequest):
    """
    Parse user context to extract structured information

    Args:
        request: ContextParsingRequest with user_context and model

    Returns:
        ContextParsingResponse with success status and parsed context
    """
    try:
        logger.info(f"[ContextController] Parsing context: {request.user_context[:50]}...")

        # Extract context
        success, parsed_context, error = context_service.extract_one_shot(
            request.user_context,
            request.model
        )

        if not success or not parsed_context:
            logger.error(f"❌ [ContextController] Parsing failed: {error}")
            return ContextParsingResponse(
                success=False,
                parsed_context=None,
                error=error or "Failed to parse context"
            )

        logger.info("✅ [ContextController] Context parsed successfully")
        return ContextParsingResponse(
            success=True,
            parsed_context=parsed_context,
            error=None
        )

    except Exception as e:
        logger.error(f"❌ [ContextController] Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@context_router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Context Parsing",
        "version": "1.0.0"
    }