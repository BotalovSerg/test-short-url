from fastapi import APIRouter
from .v1.views import router as v1_router

router = APIRouter()
router.include_router(router=v1_router)
