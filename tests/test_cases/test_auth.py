from http import HTTPStatus

from sqlalchemy import text

from auth.service import User


async def test_db_up_and_running(session):
    result = await session.execute(text("SELECT 1"))
    assert result.scalar_one() == 1


async def test_app_up_and_running(client):
    response = await client.get(url='docs')
    assert response.status_code == HTTPStatus.OK


async def test_user_registrations_success(client, session):
    response = await client.post(url='auth/sign-up', json={'username': 'test_user', 'password': 'test_password'})
    user = await User.get(session, username='test_user')

    assert user.username == 'test_user'
    assert user.password != 'test_password'
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'test_user'}


async def test_multiple_user_registration_success(client, session):
    await client.post(url='auth/sign-up', json={'username': 'some_user1', 'password': 'password1'})
    await client.post(url='auth/sign-up', json={'username': 'some_user2', 'password': 'password2'})
    users = await User.filter(session)

    assert len(users) == 2
    assert users[0].username == 'some_user1'
    assert users[1].username == 'some_user2'


async def test_user_registration_will_fail_with_duplicate_username(client, session):
    await client.post(url='auth/sign-up', json={'username': 'unique_user', 'password': 'secret_password'})
    response = await client.post(url='auth/sign-up', json={'username': 'unique_user', 'password': 'super_secret'})
    users = await User.filter(session, username='unique_user')

    assert len(users) == 1
    assert users[0].username == 'unique_user'
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': "Username 'unique_user' already taken"}


async def test_user_login_success(client):
    await client.post(url='auth/sign-up', json={'username': 'test_user', 'password': 'test_password'})
    response = await client.post(url='auth/sign-in', json={'username': 'test_user', 'password': 'test_password'})

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['access_token'], str)
    assert response.json()['token_type'] == 'bearer'


async def test_user_login_will_fail_with_wrong_password(client):
    await client.post(url='auth/sign-up', json={'username': 'test_user', 'password': 'test_password'})
    response = await client.post(url='auth/sign-in', json={'username': 'test_user', 'password': 'bad_password'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}


async def test_user_login_will_fail_with_wrong_username(client):
    await client.post(url='auth/sign-up', json={'username': 'test_user', 'password': 'test_password'})
    response = await client.post(url='auth/sign-in', json={'username': 'bad_username', 'password': 'test_password'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}


async def test_user_able_to_authenticate(client):
    await client.post(url='auth/sign-up', json={'username': 'test_user', 'password': 'test_password'})
    response = await client.post(url='auth/sign-in', json={'username': 'test_user', 'password': 'test_password'})
    access_token = response.json()['access_token']
    response = await client.get(url='auth/me', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'test_user'}


async def test_user_authentication_will_fail_with_invalid_token(client):
    await client.post(url='auth/sign-up', json={'username': 'test_user', 'password': 'test_password'})
    await client.post(url='auth/sign-in', json={'username': 'test_user', 'password': 'test_password'})
    response = await client.get(url='auth/me', headers={'Authorization': f'Bearer something_really_wrong'})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Token is invalid'}
