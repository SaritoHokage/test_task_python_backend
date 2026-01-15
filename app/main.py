from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import all_routers
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.models.video import Video 

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Videos API", lifespan=lifespan)  

for router in all_routers:
    app.include_router(router)
