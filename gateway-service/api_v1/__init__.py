from fastapi import APIRouter

from .session import session_router
from .auth import auth_router
from .profile import profile_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(session_router, prefix="/session", tags=["session"])
router.include_router(profile_router, prefix="/profile", tags=["profile"])
