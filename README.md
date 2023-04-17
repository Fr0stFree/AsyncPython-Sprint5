# Zephyr

_Zephyr_ - это пет проект, представляющий и себя файловое хранилище для различных типов файлов.

### Описание задания

Zephyr является асинхронным HTTP-сервером, обрабатывающем поступающию запросы с помощью библиотеки FastAPI.
Весь код написан в асинхронном стиле. Используется асинхронный драйвер для БД - asyncpg.
Файлы хранятся облачном хранилище Yandex S3 Objects Storage.

<details>
<summary> Список эндпоинтов </summary>

1. Статус активности связанных сервисов.

    <details>
    <summary> Подробнее </summary>
   
   **Request**
    ```
    GET /ping
    ```
    _Получить информацию по доступности сторонних сервисов (Postgresql, S3)_

   **Response**
    ```json
    {
        "database": 1.27,
        "yandex s3": 1.89
    }
    ```
   </details>


2. Регистрация пользователя.

    <details>
    <summary> Подробнее </summary>

    **Request**
    ```
    POST /users/register
    ```
    ```json
    {
        "login": "foo",
        "password": "bar"
    }
    ```
   _Регистрация нового пользователя. Запрос принимает на вход логин и пароль для создания новой учетной записи._

    </details>


3. Авторизация пользователя.

    <details>
    <summary> Подробнее </summary>

   **Request**
    ```
    POST /users/login
    ```
    ```json
    {
        "login": "foo",
        "password": "bar"
    }
    ```
   _Запрос принимает на вход логин и пароль учетной записи и возвращает авторизационный токен._
   _Далее все запросы проверяют наличие токена в заголовках - `Authorization: Bearer <token>`_

    </details>


4. Информация о загруженных файлах.

    <details>
    <summary> Подробнее </summary>

    ```
    GET storage/
    ```
    _Вернуть информацию о ранее загруженных файлах. Доступно только авторизованному пользователю._

   **Response**
    ```json
    {
        "account_id": "AH4f99T0taONIb-OurWxbNQ6ywGRopQngc",
        "files": [
              {
                "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
                "name": "notes.txt",
                "created_ad": "2020-09-11T17:22:05Z",
                "path": "/homework/test-fodler/notes.txt",
                "size": 8512,
                "is_downloadable": true
              },
            ...
              {
                "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
                "name": "tree-picture.png",
                "created_ad": "2019-06-19T13:05:21Z",
                "path": "/homework/work-folder/environment/tree-picture.png",
                "size": 1945,
                "is_downloadable": true
              }
        ]
    }
    ```
    </details>


5. Загрузить файл в хранилище.

    <details>
    <summary> Подробнее </summary>

    ```
    POST /storage/upload
    ```
    _Метод загрузки файла в хранилище. Доступно только авторизованному пользователю._
    _Для загрузки заполняется полный путь до файла, в который будет загружен/переписан загружаемый файл._
    _Если нужные директории не существуют, то они должны быть созданы автоматически._
    _Так же есть возможность указать только путь до директории._
    _В этом случае имя создаваемого файла будет создано в соответствии с передаваемым именем файла._

    **Request**
    ```
    {
        "path": <full-path-to-file>||<path-to-folder>,
    }
    ```

   **Response**
    ```json
    {
        "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
        "name": "notes.txt",
        "created_ad": "2020-09-11T17:22:05Z",
        "path": "/homework/test-fodler/notes.txt",
        "size": 8512,
        "is_downloadable": true
    }
    ```
    </details>


6. Скачать загруженный файл.

    <details>
    <summary> Подробнее </summary>
    
    **Request**
    ```
    GET /storage/download
    ```
    _Скачивание ранее загруженного файла. Доступно только авторизованному пользователю._

   **Path parameters**
    ```
    /?path=<path-to-file>||<file-meta-id>
    ```
    _Возможность скачивания есть как по переданному пути до файла, так и по идентификатору._
    </details>

</details>

### Использованные технологии

1. PostgreSQL 15.2
2. FastAPI
3. Pydantic
4. SQLAlchemy
5. Alembic
6. Pytest
7. Docker
8. Yandex S3 object storage
