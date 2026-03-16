from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logging import configure_logging
from app.db import Base, engine
import app.models  # noqa: F401
from app.routers import health

configure_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Demand Letter Bot Backend V3", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Mailing Bot V3 is running",
        "health": "/health",
        "docs": "/docs",
    }

app.include_router(health.router)