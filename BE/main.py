"""
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BE.controller.user_controller import router as user_router

# Tạo FastAPI app
app = FastAPI(
    title="Hackathon API",
    description="API cho dự án hackathon với User CRUD",
    version="1.0.0",
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


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "Hackathon API đang chạy!",
        "docs": "/docs"
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

