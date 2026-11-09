from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app import models  # noqa: F401 - register ORM models with Base metadata


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Convenient for local SQLite startup; production schema changes use Alembic.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug, lifespan=lifespan)
app.include_router(api_router)


@app.exception_handler(Exception)
async def unexpected_error_handler(_: Request, exc: Exception):
    if settings.debug:
        return JSONResponse(status_code=500, content={"detail": str(exc)})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "version": settings.app_version}
