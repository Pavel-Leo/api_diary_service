
# Project Title

A brief description of what this project does and who it's for

# api_final_yatube

### Описание

API позволяющий реализовать CRUD для проекта yatube (социальная сеть для
публикации постов)

Позволяет:
- запрашивать спиок постов. Создание нового поста. Запрашивать детализацию отдельного поста по id, его частичное или полное изменение, удаление поста.

- запрашивать спиок комментариев для определенного поста. Создание нового комментария. Запрашивать детализацию отдельного комментария по id, его частичное или полное изменение, удаление комментария.

- запрашивать список сообществ. Получение информации о сообществе по id.

- запрашивать все подписки пользователя, сделавшего запрос. Создать подписку от пользователя сделавего запрос на пользователя переданного в теле запроса.


Для аутентификации используется JWT-токены.

У неаутентифицированных пользователей доступ к API есть только на чтение.
Исключение — эндпоинт /follow/: доступ к нему предоставляется только
аутентифицированным пользователям.

Аутентифицированным пользователям разрешено изменение и удаление своего
контента; в остальных случаях доступ предоставляется только для чтения.

### Примеры запросов к API

#### Создать новый пост

```http
  POST api/v1/posts/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |
| `text` | `string` | **Required**|
| `group` | `string` | **Not required**|
| `image` | `string` | **Not rRequired**|



### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Pavel-Leo/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env (для mac и linux)
python -m venv env (для windows)
```

```
source env/bin/activate (для mac и linux)
source venv/Scripts/activate (для windows)
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip (для mac и linux)
python -m pip install --upgrade pip (для windows)
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate (для mac и linux)
python manage.py migrate (для windows)
```

Запустить проект:

```
python3 manage.py runserver (для mac и linux)
python manage.py runserver (для windows)
```


