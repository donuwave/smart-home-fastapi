from fastapi import APIRouter

from .session import session_router
from .auth import auth_router
from .profile import profile_router
from .notification import notification_router
from .home import home_router
from .device import device_router
from .face import face_router
from .stream import stream_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(session_router, prefix="/session", tags=["session"])
router.include_router(profile_router, prefix="/profile", tags=["profile"])
router.include_router(notification_router, prefix="/notification", tags=["notification"])
router.include_router(home_router, prefix="/home", tags=["home"])
router.include_router(device_router, prefix="/device", tags=['device'])
router.include_router(face_router, prefix="/face", tags=["face"])
router.include_router(stream_router, prefix='/stream', tags=['stream'])