import sys
from http import HTTPStatus

import aiofiles
import pytest

from auth.service import User
from auth.schemas import UserCreate
from storage.service import StoredFile
from storage.schemas import StoredFileCreate
from storage.constants import BUCKET_NAME


async def test_client_cannot_upload_files(session, client, dummy_file):
    async with aiofiles.open(dummy_file, mode='rb') as f:
        response = await client.post(url="/storage/upload", data={"dir": "test"}, files={"file": await f.read()})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert len(await StoredFile.filter(session)) == 0


@pytest.mark.skip
async def test_auth_client_can_upload_files(session, auth_user, dummy_file, s3_session):
    client, user = auth_user

    with open(dummy_file, 'rb') as f:
        response = await client.post(url="/storage/upload", data={"dir": "test"}, files={"file": f})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['path'] == 'test/test.txt'

    db_object = await StoredFile.get(session, user_id=user.id, path="test/test.txt")
    cloud_object = s3_session.get_object(Bucket=BUCKET_NAME, Key=str(db_object.id))

    assert cloud_object['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.OK
    assert cloud_object['ResponseMetadata']['HTTPHeaders']['content-type'] == 'application/octet-stream'
    assert cloud_object['Body'].read() == b'test'

@pytest.mark.skip
async def test_auth_client_can_specify_upload_file_options(session, auth_user, dummy_file):
    client, user = auth_user

    async with aiofiles.open(dummy_file, mode='rb') as f:
        response = await client.post(url="/storage/upload", files={"file": await f.read()},
                                     data={"dir": "test/my/ass", "name": "my_file.exe", "is_private": True})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['path'] == 'test/my/ass/my_file.exe'
    assert response.json()['name'] == 'my_file.exe'
    assert response.json()['is_private']
    assert len(await StoredFile.filter(session, user_id=user.id, path="test/my/ass/my_file.exe", is_private=True)) == 1


async def test_auth_client_cannot_upload_similar_files(session, auth_user, dummy_file):
    client, user = auth_user
    await StoredFile.create(session, StoredFileCreate(path="test/test.txt", user_id=user.id,
                                                      name="test.txt", size=sys.getsizeof(b"test")))

    async with aiofiles.open(dummy_file, mode='rb') as f:
        response = await client.post(url="/storage/upload", files={"file": await f.read()},
                                     data={"dir": "test", "name": "test.txt"})

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'File already exists'
    assert len(await StoredFile.filter(session, user_id=user.id)) == 1


async def test_client_cannot_see_storage(client):
    response = await client.get(url="/storage/")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_auth_client_can_access_storage(auth_user):
    client, user = auth_user

    response = await client.get(url="/storage/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_auth_client_can_see_storage_files(session, auth_user):
    client, user = auth_user
    file_schema_1 = StoredFileCreate(path="test/test.txt", user_id=user.id,
                                     name="test.txt", size=sys.getsizeof(b"test"))
    file_schema_2 = StoredFileCreate(path="test/test2.txt", user_id=user.id,
                                     name="test2.txt", size=sys.getsizeof(b"test_2"))
    file_schema_3 = StoredFileCreate(path="test/test3.txt", user_id=user.id,
                                     name="test3.txt", size=sys.getsizeof(b"test_huest"))
    schemas = [file_schema_1, file_schema_2, file_schema_3]
    [await StoredFile.create(session, schema) for schema in schemas]

    response = await client.get(url="/storage/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == len(schemas)
    assert [resp['name'] == schema.name for resp, schema in zip(response.json(), schemas)]
    assert [resp['path'] == schema.path for resp, schema in zip(response.json(), schemas)]
    assert [resp['user_id'] == str(user.id) for resp, schema in zip(response.json(), schemas)]
    assert [resp['size'] == schema.size for resp, schema in zip(response.json(), schemas)]


async def test_client_cannot_download_files(session, client, auth_user):
    auth_client, user = auth_user
    file = await StoredFile.create(session, StoredFileCreate(path="test/test.txt", user_id=user.id,
                                                             name="test.txt", size=sys.getsizeof(b"test")))

    response = await client.get(url="/storage/download", params={"path": file.path})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_auth_client_cannot_download_non_existing_files(session, auth_user):
    client, user = auth_user
    await StoredFile.create(session, StoredFileCreate(path="test/test.txt", user_id=user.id,
                                                      name="test.txt", size=sys.getsizeof(b"test")))

    response = await client.get(url="/storage/download", params={"path": "something_wierd"})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'File not found'}

@pytest.mark.skip
async def test_auth_client_can_download_by_path(auth_user, dummy_file):
    client, user = auth_user
    async with aiofiles.open(dummy_file, mode='rb') as f:
        await client.post(url="/storage/upload", files={"file": await f.read()},
                          data={"dir": "test/my/ass", "name": "my_file.exe"})

    response = await client.get(url="/storage/download", params={"path": "test/my/ass/my_file.exe"})

    assert response.status_code == HTTPStatus.OK
    assert response.content == b'test'
    assert response.headers['content-type'] == 'application/octet-stream'

@pytest.mark.skip
async def test_auth_client_can_download_by_id(auth_user, dummy_file):
    client, user = auth_user
    async with aiofiles.open(dummy_file, mode='rb') as f:
        response = await client.post(url="/storage/upload", files={"file": await f.read()},
                                     data={"dir": "test/my/ass", "name": "my_file.exe"})

    response = await client.get(url="/storage/download", params={"id": response.json()['id']})

    assert response.status_code == HTTPStatus.OK
    assert response.content == b'test'
    assert response.headers['content-type'] == 'application/octet-stream'


async def test_auth_clients_cannot_download_private_files(session, auth_user):
    client, user = auth_user
    another_user = await User.create(session, schema=UserCreate(username="super_boy", password="super_man"))
    file_schema = StoredFileCreate(path="test/test.txt", user_id=another_user.id, name="test.txt",
                                   size=sys.getsizeof(b"test"), is_private=True)
    private_file = await StoredFile.create(session, file_schema)

    response = await client.get(url="/storage/download", params={"path": private_file.path})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'].startswith(f'File "{private_file.name}" is private')
    assert response.headers['content-type'] != 'application/octet-stream'
