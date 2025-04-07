from fastapi import APIRouter

from .user import user_router
from .session import session_router
from .auth import auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(session_router, prefix="/session", tags=["session"])
router.include_router(user_router, prefix="/user", tags=["user"])
