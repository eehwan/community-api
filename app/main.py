from fastapi import FastAPI
from infra.database import create_tables
from routers import auth_router, board_router, post_router

app = FastAPI(
    title="커뮤니티 API",
    description="FastAPI 기반 커뮤니티 서비스",
)

app.include_router(auth_router.router)
app.include_router(board_router.router)
app.include_router(post_router.router)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "커뮤니티 서비스 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}