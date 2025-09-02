import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers.router import router


def get_application():
    _app = FastAPI(debug=settings.DEBUG, title="Document parser")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
