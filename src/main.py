import uvicorn
from fastapi import FastAPI

from auth.router import router as auth_router
from storage.router import router as storage_router
from core.router import router as core_router
from base.settings import settings


app = FastAPI(title=settings.project_name, debug=settings.debug)
app.include_router(auth_router)
app.include_router(storage_router)
app.include_router(core_router)


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=settings.server_host,
                port=settings.server_port,
                loop='asyncio',
                reload=True)
