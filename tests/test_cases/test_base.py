from http import HTTPStatus

from sqlalchemy import text



async def test_db_up_and_running(session):
    result = await session.execute(text("SELECT 1"))
    assert result.scalar_one() == 1


async def test_app_up_and_running(client):
    response = await client.get(url='docs')
    assert response.status_code == HTTPStatus.OK
