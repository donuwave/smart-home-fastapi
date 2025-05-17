from contextlib import asynccontextmanager

from fastapi import FastAPI
from config.consume import make_broker_consumer


@asynccontextmanager
async def lifespan(_: FastAPI):
    await make_broker_consumer()
    yield

app = FastAPI(lifespan=lifespan)