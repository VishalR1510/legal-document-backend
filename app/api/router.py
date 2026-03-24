from fastapi import APIRouter
from app.api.endpoints import document, query

api_router = APIRouter()

api_router.include_router(document.router, prefix="/document", tags=["Document"])
api_router.include_router(query.router, prefix="/query", tags=["Query"])
