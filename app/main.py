from fastapi import FastAPI

app = FastAPI(
    title="게시판 서비스",
    description="FastAPI 기반 게시판 서비스",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "게시판 서비스 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}