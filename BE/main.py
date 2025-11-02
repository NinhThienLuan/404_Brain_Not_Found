"""
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BE.controller.user_controller import router as user_router
from BE.controller.code_generation_controller import router as code_gen_router
from BE.controller.code_review_controller import router as code_review_router
from BE.controller.execution_log_controller import router as exec_log_router
from BE.controller.request_controller import router as request_router
from BE.controller.chat_room_controller import router as chat_room_router
from BE.controller.message_controller import router as message_router
from BE.controller.conservation_controller import router as conservation_router

# Tạo FastAPI app
app = FastAPI(
    title="Hackathon API - 404 Brain Not Found",
    description="""
    🤖 **AI-Powered Code Generation & Review Platform**
    
    ## Features:
    - 👥 **User Management** - Complete CRUD for users
    - 💬 **Conservations** - Conversation/chat management
    - 📨 **Messages** - Message CRUD with auto message count
    - 🚀 **Code Generation** - AI-powered code generation tracking
    - 🔍 **Code Review** - Code review results & analysis
    - 📊 **Execution Logs** - Compile, test, lint results
    - 📝 **Request Management** - User requirement tracking
    - 🏠 **Chat Rooms** - Chat room management
    
    ## Entity-based Architecture:
    - Clean Architecture with Domain Entities
    - Repository Pattern for data access
    - Service Layer for business logic
    - RESTful API endpoints
    """,
    version="2.0.0",
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

# Register routers
app.include_router(user_router)
app.include_router(conservation_router)
app.include_router(message_router)
app.include_router(code_gen_router)
app.include_router(code_review_router)
app.include_router(exec_log_router)
app.include_router(request_router)
app.include_router(chat_room_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "🤖 Hackathon API - 404 Brain Not Found",
        "version": "2.0.0",
        "endpoints": {
            "users": "/api/users",
            "conservations": "/api/conservations",
            "messages": "/api/messages",
            "code_generations": "/api/code-generations",
            "code_reviews": "/api/code-reviews",
            "execution_logs": "/api/execution-logs",
            "requests": "/api/requests",
            "chat_rooms": "/api/chat-rooms"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "BE.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload khi code thay đổi
    )

