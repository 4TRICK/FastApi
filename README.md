[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=📝+FastAPI+Notes+Management+API)](https://git.io/typing-svg)

# Подготовка к запуску и запуск
В качестве БД используется mongoDB.  
В репозиторий НАМЕРЕННО вынесены .env файлы:
- в корневой директории .env используется для тестов (TESTING=True);
- в src/ .env используется для запуска локально через main.py или команду;
- в src/ .env.docker и .env.mongo.docker используется для запуска через docker-compose.

Есть несколько способов запуска:
- запуск файла main.py
- запуск командой ```uvicorn src.app:app --reload```
- через Docker ```docker-compose up -d --build```
- особняком находится запуск тестов ```coverage run -m pytest``` 

Локально доступ через порт 8000, через Docker - 8011

# Тестирование
Для запуска тестов используется команда```coverage run -m pytest```  
Для проверки покрытия используется команда```coverage report -m```  
На данный момент покрытие 96%  

## 📚 Возможности по ролям

### 👤 Пользователь (`user`)
- Может создавать, изменять, удалять, просматривать **только свои** заметки

### 👨‍💼 Администратор (`admin`)
- Может просматривать все заметки
- Может восстанавливать удалённые заметки

## Регистрация

В системе реализована два типа пользователя: `user` и `admin`.  
Чтобы начать пользоваться системой, необходимо выполнить регистрацию.  
Во время регистрации необходимо указать поля `email`, `password` и **опционально** `is_admin` для создания учетной записи администратора (по умолчанию `false`).  
**URL для регистрации:** `POST /auth/register`

### Пример регистрации
```python
import requests

url = 'http://localhost:8011/auth/register'
body = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "qwerty"
}
res = requests.post(url, json=body)
print(res.json())
```

---

## Авторизация

Авторизация в системе выполнена на основе JWT.  
Для авторизации необходимо указать поля `email`, `password`.  
При успешном запросе вернется ответ с полями `access_token` и `token_type`.  
> ⚠️ ВНИМАНИЕ! `refresh_token` в данной реализации отсутствует  
**URL для получения access_token:** `POST /auth/token`

### Пример авторизации
```python
url = 'http://localhost:8011/auth/token'
body = {
    "email": "user1@example.com",
    "password": "qwerty"
}
res = requests.post(url, json=body)
print(res.json())
token = res.json().get("access_token")
```

---

## Просмотр текущего пользователя

**URL для просмотра текущего пользователя:** `GET /auth/user`  
(Требуется передать `Bearer` токен)

### Пример
```python
url = 'http://localhost:8011/auth/user'
headers = {'Authorization': f'Bearer {token}'}
res = requests.get(url, headers=headers)
print(res.json())
```

---

# Заметки

Для доступа к любой функции работы с заметками необходимо указать `Bearer` токен!  
Любая заметка состоит из:
- обязательного поля `title` (максимальная длина 256 символов)
- опционального поля `body` (максимальная длина 65536 символов)

---

## Создание заметки

Доступно только для пользователя типа `user`.  
**URL:** `POST /notes`

### Пример
```python
url = 'http://localhost:8011/notes'
headers = {'Authorization': f'Bearer {token}'}
body = {
    "title": "Моя первая заметка",
    "body": "Содержимое"
}
res = requests.post(url, headers=headers, json=body)
print(res.json())
```

---

## Просмотр всех заметок

- `admin`: при запросе без параметров — все заметки всех пользователей  
- `admin`: с параметром `notes_user_id` — заметки конкретного пользователя  
- `user`: без параметров — свои заметки  
- `user`: с параметром `notes_user_id`, если равен текущему ID — свои заметки  
- `user`: с чужим `notes_user_id` — ❌ доступ запрещен  

**URL без параметра:** `GET /notes`  
**URL с параметром:** `GET /notes?notes_user_id=<user_id>`

### Пример
```python
url = 'http://localhost:8011/notes'
headers = {'Authorization': f'Bearer {token}'}
res = requests.get(url, headers=headers)
print(res.json())
```

---

## Просмотр конкретной заметки

- `admin`: всегда доступ  
- `user`: доступ только к своей заметке  
**URL:** `GET /notes/{note_id}`

### Пример
```python
note_id = "SOME_NOTE_ID"
url = f'http://localhost:8011/notes/{note_id}'
headers = {'Authorization': f'Bearer {token}'}
res = requests.get(url, headers=headers)
print(res.json())
```

---

## Обновление заметки

Доступно только для пользователя типа `user`, если он владелец.  
**URL (PUT):** `PUT /notes/{note_id}`  
**URL (PATCH):** `PATCH /notes/{note_id}`

### Пример (PUT)
```python
url = f'http://localhost:8011/notes/{note_id}'
headers = {'Authorization': f'Bearer {token}'}
body = {
    "title": "Обновленный заголовок",
    "body": "Новое содержимое"
}
res = requests.put(url, headers=headers, json=body)
print(res.json())
```

---

## Удаление заметки

Доступно только для пользователя типа `user`, если он владелец.  
**URL:** `DELETE /notes/{note_id}`

### Пример
```python
url = f'http://localhost:8011/notes/{note_id}'
headers = {'Authorization': f'Bearer {token}'}
res = requests.delete(url, headers=headers)
print(res.status_code)
```

---

## Восстановление удаленной заметки

Доступно только для пользователя типа `admin`.  
Если заметка с переданным ID существует среди удаленных — она будет восстановлена.  
**URL:** `GET /notes/restore/{note_id}`

### Пример
```python
url = f'http://localhost:8011/notes/restore/{note_id}'
headers = {'Authorization': f'Bearer {admin_token}'}
res = requests.get(url, headers=headers)
print(res.json())
```
