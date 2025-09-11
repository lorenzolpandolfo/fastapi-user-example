from fastapi.routing import APIRouter

from losocial.web.api import dog, dummy, echo, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(dog.router, prefix="/dog", tags=["dog"])
