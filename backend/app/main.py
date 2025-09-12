from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import get_settings
from .api.routes.transcripts import router as transcripts_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="YouTube Channel Q&A Backend", version="0.1.0")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(transcripts_router, prefix="/api")

    return app


app = create_app()


