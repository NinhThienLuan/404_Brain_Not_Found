"""
Main FastAPI Application - Messages & Conservations Only
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BE.controller.message_controller import router as message_router
from BE.controller.conservation_controller import router as conservation_router

# Tạo FastAPI app
app = FastAPI(
    title="Chatbox API - 404 Brain Not Found",
    description="""
    💬 **Messages & Conservations API**
    
    ## Features:
    - 💬 **Conservations** - Conversation/chat management
    - 📨 **Messages** - Message CRUD with auto message count
    - 🔗 **Nested Endpoints** - RESTful chatbox integration
    
    ## Architecture:
    - Clean Architecture với Entity-based Design
    - Repository Pattern for database access
    - Service Layer with business logic
    - Auto message count sync
    - Cascade delete support
    
    ## Chatbox Features:
    - ✅ POST /api/conservations/{id}/messages - Add message
    - ✅ DELETE /api/conservations/{id}/messages/{mid} - Remove message
    - ✅ GET /api/conservations/{id}/with-messages - Load full chat
    - ✅ Auto update message count
    - ✅ Search conservations
    - ✅ Add facts to conservations
    """,
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên giới hạn origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers - CHỈ Messages & Conservations
app.include_router(conservation_router)
app.include_router(message_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "💬 Chatbox API - 404 Brain Not Found",
        "version": "3.0.0",
        "features": [
            "Conservations management",
            "Messages CRUD",
            "Auto message count",
            "Nested endpoints for chatbox",
            "Search & filter",
            "Cascade delete"
        ],
        "endpoints": {
            "conservations": "/api/conservations",
            "messages": "/api/messages"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Chatbox API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "BE.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
