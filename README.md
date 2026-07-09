# Django Simple CRUD API Documentation

## Overview
This Django project exposes a basic REST API for user management and todo tasks.
The API is served under `/api/`.

## Getting Started
1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Install dependencies if needed:
   ```bash
   python -m pip install -r requirements.txt
   ```
   > If `requirements.txt` is not present, install manually:
   > `python -m pip install Django djangorestframework djangorestframework-simplejwt`
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## Root endpoints
- `GET /` - Returns a JSON welcome message and points to the API root.
- `GET /api/` - Returns the API root JSON response.

## Authentication
- This project uses JWT authentication via `djangorestframework-simplejwt`.
- Login returns `access` and `refresh` tokens.
- Protected endpoints require the header:
  ```http
  Authorization: Bearer <access_token>
  ```

## Endpoints

### User registration
- `POST /api/user/create/`
- Creates a new user and returns JWT tokens.
- Request body example:
  ```json
  {
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepassword",
    "age": 30
  }
  ```

### Login
- `POST /api/login/`
- Authenticates an existing user and returns JWT tokens.
- Request body example:
  ```json
  {
    "email": "alice@example.com",
    "password": "securepassword"
  }
  ```

### Refresh token
- `POST /api/token/refresh/`
- Request body example:
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

### Get a user by ID
- `GET /api/user/<id>/`
- Returns mock/dummy user data for IDs 1, 2, and 3.
- This endpoint is not authenticated.

### Get all users
- `GET /api/all/users/`
- Requires authentication.
- Returns all user records from the database.

### Update or delete a user
- `PATCH /api/user/update/<id>/`
- `DELETE /api/delete/user/<id>/`
- Both require authentication.
- Update request body example:
  ```json
  {
    "email": "newemail@example.com",
    "age": 31
  }
  ```

### Todo tasks
- `GET /api/tasks/` - List tasks for the authenticated user.
- `POST /api/tasks/` - Create a new task for the authenticated user.

  Request body example:
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }
  ```

- `GET /api/tasks/<id>/` - Retrieve a specific task.
- `PATCH /api/tasks/<id>/` - Update a specific task.
- `DELETE /api/tasks/<id>/` - Delete a specific task.

## Notes
- The project uses a custom `api.User` model with `email` as the `USERNAME_FIELD`.
- `Todo` and `User` models use `BigAutoField` by default due to `DEFAULT_AUTO_FIELD` in `newproject/settings.py`.

## Example curl usage
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "securepassword"}'
```

```bash
curl http://127.0.0.1:8000/api/ \
  -H "Authorization: Bearer <access_token>"
```
