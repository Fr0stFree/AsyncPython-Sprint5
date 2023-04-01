import sys
from http import HTTPStatus

from auth.service import User
from auth.schemas import UserCreate
from storage.service import StoredFile
from storage.schemas import StoredFileCreate


async def test_client_cannot_upload_files(session, client, dummy_file):
    with open(dummy_file, 'rb') as f:
        response = await client.post(url="/storage/upload", data={"dir": "test"}, files={"file": f})
    files = await StoredFile.filter(session)
    
    assert len(files) == 0
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_auth_client_can_upload_files(session, auth_user, dummy_file):
    client, user = auth_user
    with open(dummy_file, 'rb') as f:
        response = await client.post(url="/storage/upload", data={"dir": "test"}, files={"file": f})
        
    files = await StoredFile.filter(session, user_id=user.id, path="test/test.txt")
    
    assert len(files) == 1
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['path'] == 'test/test.txt'


async def test_auth_client_can_specify_upload_file_options(session, auth_user, dummy_file):
    client, user = auth_user
    with open(dummy_file, 'rb') as f:
        response = await client.post(url="/storage/upload", files={"file": f},
                                     data={"dir": "test/my/ass", "name": "my_file.exe", "is_private": True})
        
    files = await StoredFile.filter(session, user_id=user.id, path="test/my/ass/my_file.exe", is_private=True)

    assert len(files) == 1
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['path'] == 'test/my/ass/my_file.exe'
    assert response.json()['name'] == 'my_file.exe'
    assert response.json()['is_private']
    assert response.json()['id'] == str(files[0].id)
    

async def test_auth_client_cannot_upload_similar_files(session, auth_user, dummy_file):
    client, user = auth_user
    file_schema = StoredFileCreate(path="test/test.txt", user_id=user.id, content=b"test",
                                   name="test.txt", size=sys.getsizeof(b"test"))
    await StoredFile.create(session, file_schema)

    with open(dummy_file, 'rb') as f:
        response = await client.post(url="/storage/upload", files={"file": f},
                                     data={"dir": "test", "name": "test.txt"})
    files = await StoredFile.filter(session, user_id=user.id)
    
    assert len(files) == 1
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'File already exists'
    

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
    file_schema_1 = StoredFileCreate(path="test/test.txt", user_id=user.id, content=b"test",
                                     name="test.txt", size=sys.getsizeof(b"test"))
    file_schema_2 = StoredFileCreate(path="test/test2.txt", user_id=user.id, content=b"test_2",
                                     name="test2.txt", size=sys.getsizeof(b"test_2"))
    file_schema_3 = StoredFileCreate(path="test/test3.txt", user_id=user.id, content=b"test_huest",
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
    file_schema = StoredFileCreate(path="test/test.txt", user_id=user.id, content=b"test",
                                   name="test.txt", size=sys.getsizeof(b"test"))
    file = await StoredFile.create(session, file_schema)
    
    response = await client.get(url="/storage/download", params={"path": file.path})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_auth_client_cannot_download_non_existing_files(session, auth_user):
    client, user = auth_user
    file_schema = StoredFileCreate(path="test/test.txt", user_id=user.id, content=b"test",
                                   name="test.txt", size=sys.getsizeof(b"test"))
    await StoredFile.create(session, file_schema)
    
    response = await client.get(url="/storage/download", params={"path": "something_wierd"})
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'File not found'}


async def test_auth_client_can_download_by_path(session, auth_user):
    client, user = auth_user
    file_schema = StoredFileCreate(path="test/test.txt", user_id=user.id, content=b"test",
                                   name="test.txt", size=sys.getsizeof(b"test"))
    file = await StoredFile.create(session, file_schema)
    
    response = await client.get(url="/storage/download", params={"path": file.path})
    
    assert response.status_code == HTTPStatus.OK
    assert response.content == b'test'
    assert response.headers['content-type'] == 'application/octet-stream'


async def test_auth_client_can_download_by_id(session, auth_user):
    client, user = auth_user
    file_schema = StoredFileCreate(path="test/test.txt", user_id=user.id, content=b"test",
                                   name="test.txt", size=sys.getsizeof(b"test"))
    file = await StoredFile.create(session, file_schema)
    
    response = await client.get(url="/storage/download", params={"id": str(file.id)})
    
    assert response.status_code == HTTPStatus.OK
    assert response.content == b'test'
    assert response.headers['content-type'] == 'application/octet-stream'
    

async def test_auth_clients_cannot_download_private_files(session, auth_user):
    client, user = auth_user
    another_user = await User.create(session, schema=UserCreate(username="super_boy", password="super_man"))
    file_schema = StoredFileCreate(path="test/test.txt", user_id=another_user.id, content=b"test",
                                   name="test.txt", size=sys.getsizeof(b"test"), is_private=True)
    private_file = await StoredFile.create(session, file_schema)
    
    response = await client.get(url="/storage/download", params={"path": private_file.path})
    
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'].startswith(f'File "{private_file.name}" is private')
    assert response.headers['content-type'] != 'application/octet-stream'
