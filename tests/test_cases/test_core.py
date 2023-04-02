from http import HTTPStatus


async def test_ping_services(client):
    response = await client.get(url='services/ping')

    assert response.status_code == HTTPStatus.OK
    
    db_status = next(filter(lambda x: x['name'] == 'database', response.json()), None)
    
    assert db_status is not None
    assert db_status.get('status') == 'ACTIVE'
    assert isinstance(db_status.get('ping'), float)
    