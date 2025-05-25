import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_v1.device.repository import DeviceRepository
from api_v1.face.repository import FaceRepository
from api_v1.stream.service import StreamService
from config.consume import make_broker_consumer
from api_v1 import router as router_v1
from config.database import db_helper


@asynccontextmanager
async def lifespan(_: FastAPI):
    await make_broker_consumer()

    session = db_helper.session_factory()  # AsyncSession
    try:
        device_repo = DeviceRepository(db_session=session)
        face_repo = FaceRepository(db_session=session)

        svc = StreamService(
            device_repository=device_repo,
            face_repository=face_repo
        )

        devices = await device_repo.get_all_device()
        for cam in devices:
            asyncio.create_task(
                svc.start_processing(
                    home_id=cam.home_id,
                    device_id=cam.id
                ),
                name=f"camera-detector-{cam.id}"
            )
            print(f"[Startup] Детектор для камеры {cam.id} запущен в фоне")

    finally:
        await session.close()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix='/api/v1')