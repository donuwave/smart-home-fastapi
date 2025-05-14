from contextlib import asynccontextmanager

from fastapi import FastAPI
from config.consume import make_broker_consumer
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await make_broker_consumer()
    yield

app = FastAPI(lifespan=lifespan, title="Notification Service")
