from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes import router
from src.config import settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=True
    )