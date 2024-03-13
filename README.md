# Сервер для игры в сет (json)
## Важные пометки!
1. Файл с названием `users.json` и основной код `main.py` должны находится в одной директории.
2. В директории `set/searchSet` присутсвует отдельная программа для поиска сета. Там также находится файл `cards2.json` и основной код `main.py` они должны находится в одной директории.

## Установка
### Скачать данные
Кликнуть на `Code` -> `Download ZIP` чтобы скачать архив. После чего извлечь данные.

Сервер создан со стороны разработчика и дизайна в нем никагого ни присутствует. Поэтому вам может пригодится приложения для отправления запросов и получение ответа. В своем проекте я использовала приложение Postman для этих целей.

## Установка зависимостей
Запустить консоль. Перейти в папку проекта. При необходимости прописать полный путь (`cd D:/.../.../Папка_Проекта`)

`cd <Папка_Проекта>
pip install flask`

## Использование
Запуск приложения осуществляется также в консоли
`python main_server.py`
После чего Вы можете отправлять запросы на локальный адрес http://127.0.0.1:5000/ 
Например:
по адресу http://127.0.0.1:5000/user/register

## Взаимодействие с сервером

### Регистрация
`/user/register`

Запрос
```
{
    "nickname":"user-test",
    "password":"user123"
}
```
Ответ
```
{
    "nickname": "user-test",
    "accessToken": "f872a167c9b0"
}
```

### Игра
Создать
`/set/room/create`

Запрос
```
{
    "accessToken":"f872a167c9b0"
}
```
Ответ
```
{
    "success": true,
    "exception": null,
    "gameId": 0
}
```
### Список игр
`/set/room/list`

Запрос
```
{
    "accessToken":"f872a167c9b0"
}
```
Ответ
```
{
    "games": [
        {
            "id": 1
        }
    ]
}
```

### Войти в игру
`/set/room/enter`

Запрос
```
{
    "accessToken":"f872a167c9b0",
    "gameId": 1
}
```
Ответ
```
{
    "success": true,
    "exception": null,
    "gameId": 1
}
```

## Когда пользователь находится в игре

### Поле
`/set/field`

Запрос
```
{
    "accessToken":"f872a167c9b0"
}
```
Ответ
```
{
    "cards": [
        {
            "id": 6,
            "color": 1,
            "shape": 2,
            "fill": 3,
            "count": 1
        },
        {
            "id": 21,
            "color": 3,
            "shape": 1,
            "fill": 3,
            "count": 2
        },
        {
            "id": 3,
            "color": 1,
            "shape": 1,
            "fill": 3,
            "count": 3
        },
        {
            "id": 24,
            "color": 3,
            "shape": 2,
            "fill": 3,
            "count": 1
        },
        {
            "id": 15,
            "color": 2,
            "shape": 2,
            "fill": 3,
            "count": 2
        },
        {
            "id": 5,
            "color": 1,
            "shape": 2,
            "fill": 2,
            "count": 3
        },
        {
            "id": 25,
            "color": 3,
            "shape": 3,
            "fill": 1,
            "count": 1
        },
        {
            "id": 27,
            "color": 3,
            "shape": 3,
            "fill": 3,
            "count": 2
        },
        {
            "id": 10,
            "color": 2,
            "shape": 1,
            "fill": 1,
            "count": 3
        }
    ],
    "status": "ongoing",
    "score": 0
}
```
Статус может быть `ongoing` или `ended`

### Выбрать
`/set/pick`

Запрос
```
{
    "accessToken":"f872a167c9b0",
    "cards":[
        5, 10, 25
    ]
}
```
Ответ
```
{
    "isSet": false,
    "score": 0
}
```

### Добавить
Добавить карты на поле

`/set/add`

Запрос
```
{
    "accessToken":"f872a167c9b0",
}
```
Ответ
```
{
    "success": true,
    "exception": null
}
```

### Баллы
Добавить карты на поле

`/set/scores`

Запрос
```
{
    "accessToken":"f872a167c9b0",
}
```
Ответ
```
{
    "success": true,
    "exception": null,
    "users": [
        {
            "name": "Sergey",
            "score": 12
        },
        {
            "name": "user-test",
            "score": 0
        }
    ]
}
```
## Как пользоватся программаой для поиска сета?
Этот код работает вне сервера. Просто небольшая помощь, когда вы не можете найти сет.
1. Копируете поле и вставляете в файл `cards2.json`.Незабудь потом сохранить файл с изменениями. Например
```
{
    "cards": [
        {
            "id": 6,
            "color": 1,
            "shape": 2,
            "fill": 3,
            "count": 1
        },
        {
            "id": 21,
            "color": 3,
            "shape": 1,
            "fill": 3,
            "count": 2
        },
        {
            "id": 3,
            "color": 1,
            "shape": 1,
            "fill": 3,
            "count": 3
        },
        {
            "id": 24,
            "color": 3,
            "shape": 2,
            "fill": 3,
            "count": 1
        },
        {
            "id": 15,
            "color": 2,
            "shape": 2,
            "fill": 3,
            "count": 2
        },
        {
            "id": 5,
            "color": 1,
            "shape": 2,
            "fill": 2,
            "count": 3
        },
        {
            "id": 25,
            "color": 3,
            "shape": 3,
            "fill": 1,
            "count": 1
        },
        {
            "id": 27,
            "color": 3,
            "shape": 3,
            "fill": 3,
            "count": 2
        },
        {
            "id": 10,
            "color": 2,
            "shape": 1,
            "fill": 1,
            "count": 3
        }
    ],
    "status": "ongoing",
    "score": 0
}
```
2. дальше запускаете код в файле `main.py` из директории `searchSet`.
