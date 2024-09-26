from fastapi import APIRouter
from app.api.api_v1.endpoints import aadhar

api_router = APIRouter()

api_router.include_router(aadhar.router, prefix="/aadhar", tags=["Aadhar"])
