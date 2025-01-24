from fastapi import FastAPI
import uvicorn
from routers.health import router as health_router
from routers.llm import router as llm_router

app = FastAPI()

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(llm_router, prefix="/llm", tags=["llm"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
