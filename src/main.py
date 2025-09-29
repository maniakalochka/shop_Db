import logging
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from db.session import engine, SessionLocal
from routers.api import api_router

log = logging.getLogger(__name__)


@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    log.info("Starting up...")
    app.state.engine = engine  # type: ignore
    app.state.session_factory = SessionLocal  # type: ignore
    yield
    log.info("Shutting down...")
    await engine.dispose()


app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000)
