from app.api.health import router as health_router
from app.api.videos import router as videos_router

all_routers = (health_router, videos_router)
