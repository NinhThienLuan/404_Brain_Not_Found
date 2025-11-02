"""
Main FastAPI Application - Messages & Conservations Only
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BE.controller.message_controller import router as message_router
from BE.controller.conservation_controller import router as conservation_router
from BE.controller.ai_controller import ai_router
from BE.controller.agent_controller import agent_router

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
    version="2.0.0",
    title="Hackathon API - AI Agent Orchestration",
    description="API cho dự án hackathon với AI Agent Orchestration, Code Generation và User Management",
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

# Register routers - CHỈ Messages & Conservations
app.include_router(conservation_router)
app.include_router(message_router)
app.include_router(code_gen_router)
app.include_router(code_review_router)
app.include_router(exec_log_router)
app.include_router(request_router)
app.include_router(chat_room_router)
app.include_router(ai_router)
app.include_router(agent_router)


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
        "message": "Hackathon API đang chạy!",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "User Management (/api/users)",
            "AI Code Generation (/ai)",
            "Agent Orchestration (/agent)"
        ],
        "endpoints": {
            "users": "/api/users",
            "ai_generate": "/ai/generate",
            "ai_review": "/ai/review",
            "agent_session": "/agent/session/create",
            "agent_parse_context": "/agent/context/parse",
            "agent_process_prompt": "/agent/prompt/process",
            "agent_analyze_code": "/agent/code/analyze"
        }
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
