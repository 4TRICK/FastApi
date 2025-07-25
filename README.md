# 📝 FastAPI Notes Management API

## 📌 Описание

API для управления заметками с JWT-аутентификацией и ролевой моделью (`user` и `admin`).

---

## ⚙️ Установка и запуск

### 💼 Требования

- Python 3.9+
- MongoDB
- Docker (опционально)

### 🗂️ Конфигурация `.env`

В проекте уже предусмотрены конфигурации:
- `.env` — для тестов (корень проекта)
- `src/.env` — для локального запуска
- `src/.env.docker` и `.env.mongo.docker` — для Docker

### 🔧 Установка

```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows
pip install -r requirements.txt
```

### 🚀 Запуск API

**1. Локально:**

```bash
python src/main.py
# или
uvicorn src.app:app --reload
```

**2. Через Docker:**

```bash
docker-compose up -d --build
```

### 📡 Порты доступа

- Локально: `http://localhost:8000`
- Через Docker: `http://localhost:8011`

---

## 🔐 Авторизация

### 🔸 Регистрация пользователя

```python
import requests

url = 'http://localhost:8011/auth/register'
body = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "qwerty"
}

response = requests.post(url, json=body)
print(response.json())
```

### 🔸 Получение токена

```python
url = 'http://localhost:8011/auth/token'
body = {
    "email": "user1@example.com",
    "password": "qwerty"
}

response = requests.post(url, json=body)
print(response.json())
```

### 🔸 Получение текущего пользователя

```python
url = 'http://localhost:8011/auth/user'
headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}

response = requests.get(url, headers=headers)
print(response.json())
```

---

## 🗃️ Работа с заметками

### 🔸 Создание заметки (только для `user`)

```python
url = 'http://localhost:8011/notes'
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}
body = {
    "title": "Заголовок",
    "body": "Текст заметки"
}

response = requests.post(url, headers=headers, json=body)
print(response.json())
```

### 🔸 Получение всех заметок

```python
url = 'http://localhost:8011/notes'
headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}

response = requests.get(url, headers=headers)
print(response.json())
```

#### Для `admin` — заметки конкретного пользователя:

```python
params = {'notes_user_id': 'USER_ID'}
response = requests.get(url, headers=headers, params=params)
print(response.json())
```

### 🔸 Получение конкретной заметки

```python
note_id = 'NOTE_ID'
url = f'http://localhost:8011/notes/{note_id}'
response = requests.get(url, headers=headers)
print(response.json())
```

### 🔸 Обновление заметки

```python
url = f'http://localhost:8011/notes/{note_id}'
body = {
    "title": "Новый заголовок",
    "body": "Новый текст"
}

response = requests.put(url, headers=headers, json=body)
print(response.json())
```

### 🔸 Удаление заметки

```python
response = requests.delete(url, headers=headers)
print(response.status_code)
```

### 🔸 Восстановление заметки (только `admin`)

```python
url = f'http://localhost:8011/notes/restore/{note_id}'
admin_headers = {'Authorization': 'Bearer ADMIN_ACCESS_TOKEN'}

response = requests.get(url, headers=admin_headers)
print(response.json())
```

---

## 🧪 Тестирование

```bash
coverage run -m pytest
coverage report -m
```

📈 Текущее покрытие: **96%**

---

## 📓 Swagger и Redoc

- Swagger UI: `http://localhost:8000/docs` или `http://localhost:8011/docs`
- Redoc: `http://localhost:8000/redoc` или `http://localhost:8011/redoc`

---

## 🛠️ Пример ответа (создание заметки)

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Моя заметка",
  "body": "Содержимое заметки",
  "owner": "user@example.com",
  "created_at": "2023-01-01T00:00:00"
}
```

---

## 📚 Возможности по ролям

### 👤 Пользователь (`user`)
- Может создавать, изменять, удалять, просматривать **только свои** заметки

### 👨‍💼 Администратор (`admin`)
- Может просматривать все заметки
- Может восстанавливать удалённые заметки

---

## 📁 Логирование

Все действия логируются в `app.log`.