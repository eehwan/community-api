from fastapi import FastAPI
from infra.database import create_tables
from routers import user_router, board_router, post_router

app = FastAPI(
    title="미니 프로젝트",
    description="FastAPI 기반 게시판 서비스",
)

app.include_router(user_router.router)
app.include_router(board_router.router)
app.include_router(post_router.router)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "게시판 서비스 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}