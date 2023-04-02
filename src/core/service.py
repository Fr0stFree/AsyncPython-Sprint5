import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession


async def ping_db(session: AsyncSession) -> float | None:
    start_time: float = time.time()
    try:
        await session.execute(text("SELECT 1"))
        return round(time.time() - start_time, 2) * 1000
    except OperationalError:
        return None
