from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from controller.ai_controller import ai_router
from utils.config import env


def create_app() -> FastAPI:
    """
    Application factory pattern for FastAPI
    Creates and configures the FastAPI application
    """
    # Create FastAPI instance
    app = FastAPI(
        title=env.APP_NAME,
        description="AI Agent for Code Generation and Review using Google Gemini",
        version="2.0.0",
        docs_url=f"{env.PREFIX_API}/docs",
        redoc_url=f"{env.PREFIX_API}/redoc",
        openapi_url=f"{env.PREFIX_API}/openapi.json"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=env.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(ai_router, prefix=env.PREFIX_API)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information"""
        return {
            "message": env.APP_NAME,
            "version": "2.0.0",
            "status": "running",
            "endpoints": {
                "generate": f"{env.PREFIX_API}/ai/generate",
                "review": f"{env.PREFIX_API}/ai/review",
                "parse_context": f"{env.PREFIX_API}/context/parse",
                "classify_intent": f"{env.PREFIX_API}/intent/classify",
                "health": f"{env.PREFIX_API}/ai/health",
                "docs": f"{env.PREFIX_API}/docs",
                "redoc": f"{env.PREFIX_API}/redoc"
            },
            "config": {
                "app_name": env.APP_NAME,
                "port": env.PORT,
                "debug": env.DEBUG,
                "api_prefix": env.PREFIX_API
            }
        }
    
    # Health check endpoint at root level
    @app.get("/health", tags=["Root"])
    async def health():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": env.APP_NAME
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    print("=" * 60)
    print(f" Starting {env.APP_NAME}")
    print("=" * 60)
    print(f"Server URL: http://{env.HOST}:{env.PORT}")
    print(f"API Docs: http://{env.HOST}:{env.PORT}{env.PREFIX_API}/docs")
    print(f"ReDoc: http://{env.HOST}:{env.PORT}{env.PREFIX_API}/redoc")
    print(f"Debug mode: {env.DEBUG}")
    print(f"API Key: {env.GEMINI_API_KEY[:8]}..." if env.GEMINI_API_KEY else "No API Key")
    print(f"CORS Origins: {', '.join(env.CORS_ORIGINS)}")
    print("=" * 60)
    
    # Run with uvicorn
    uvicorn.run(
        "app:app",
        host=env.HOST,
        port=env.PORT,
        reload=env.DEBUG,
        log_level="info" if not env.DEBUG else "debug"
    )
