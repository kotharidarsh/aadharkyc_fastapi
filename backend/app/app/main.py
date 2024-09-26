from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from app.api.utils.exception_handler import register_handlers
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=settings.API_VERSION_STR + "/openapi.json",
    version=settings.VERSION,
    middleware=settings.MIDDLEWARES,
    docs_url=settings.API_VERSION_STR + "/docs",
    redoc_url=settings.API_VERSION_STR + "/redoc"
)

register_handlers(app)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_VERSION_STR)
