from fastapi import APIRouter

from src.app.api.v1 import flows

router = APIRouter()
router.include_router(flows.router)
