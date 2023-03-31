import uvicorn
from fastapi import FastAPI

from auth.router import router as auth_router
from storage.router import router as storage_router
from base.settings import settings


app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
app.include_router(auth_router)
app.include_router(storage_router)


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                loop='asyncio',
                reload=True)
