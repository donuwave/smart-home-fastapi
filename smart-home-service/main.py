from contextlib import asynccontextmanager

from fastapi import FastAPI
from config.consume import make_broker_consumer
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(_: FastAPI):
    await make_broker_consumer()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix='/api/v1')