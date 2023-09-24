# FastAPI project: Advertisement Service

---

## Stack:
>  - FastApi=0.103.1
>  - FastApi Users
>  - alembic
>  - SQLAlchemy
>  - asyncpg

---

## Description

### API service for advertisement service

* ##### Get all advertisements (ads) types (GET): http://localhost:8000/api/v1/ad/type/
* ##### Get type by id (GET) params={type_id}: http://localhost:8000/api/v1/ad/types/{type_id}/
* ##### Add type (POST) **only for admin** params={type_name}: http://localhost:8000/api/v1/ad/{type_name}/
* ##### Get all ads categories (GET): http://localhost:8000/api/v1/ad/category/
* ##### Add category (POST) **only for admin** params={cat_name}: http://localhost:8000/api/v1/ad/{cat_name}/
* ##### Get all ads with pagination (GET) params={page=0, size=5}: http://localhost:8000/api/v1/ad/?page={page}&size={size}
* ##### Get ad by id (GET) params={ad_id}: http://localhost:8000/api/v1/ad/{ad_id}/
* ##### Get ads by type with pagination (GET) params={type_id, page=0, size=5}: http://localhost:8000/api/v1/ad/type/{type_id}/?page={page}&size={size}
* ##### Get ads by category name (GET) params={category_name}: http://localhost:8000/api/v1/ad/{category_name}/
* ##### Add ad (POST) **only for auth user**: http://localhost:8000/api/v1/ad/. Response body:
```
{
  "name": "string",
  "category_id": 0,
  "description": "string",
  "price": "string",
  "created_at": "2023-09-24T11:35:40.077595",
  "updated_at": "2023-09-24T11:35:40.077595",
  "user_id": 0
}
```
* #### Update ad (PUT) 
* #### Delete ad (DELETE) **only for owner and admin** params={ad_id}:  http://localhost:8000/api/v1/ad/delete/{ad_id}/
* #### Get all comments (GET) params={ad_id}:  http://localhost:8000/api/v1/ad/{ad_id}/comments/
* #### Add comment (POST) **only for auth user** params={ad_id}:  http://localhost:8000/api/v1/ad/{ad_id}/comments/
* #### Delete comment (DELETE) **only admin** params=[{ad_id}, {comment_id}]:  http://localhost:8000/api/v1/ad/{ad_id}/comments/delete/{comment_id}/

---

## Auth Block

### Login with JWT

* #### Sign up (POST): http://localhost:8000/api/v1/auth/register/. Response body:
```
{
  "email": "email@email.com",
  "password": "password",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "username": "string",
  "role_id": 0,
  "is_banned": false
}
```

* #### Login (POST): http://localhost:8000/api/v1/auth/jwt/login/. Response body:
```
{
  "username": "email@email.com",
  "password": "password",
}
```
* #### Logout (POST): http://localhost:8000/api/v1/auth/jwt/logout/

* #### Banned user **only for admin** (POST) params={user_id}: http://localhost:8000/api/v1/auth/banned/{user_id}}/
* #### Make admin user **only for admin** (POST) params={user_id}: http://localhost:8000/api/v1/auth/make_admin/{user_id}}/

---

## * Also You can see in swagger UI (/docs)

---
---

## Frontend: http://localhost:8000/

---
### Start project
```
python -m venv venv
```
```
venv\Scripts\activate
```
```
pip install -r requrements.txt
```
```
alembic revision --autogenerate -m "Name of migration"
```
```
alembic upgrade head
```
```
uviron src.main:app --reload for debug
```
---

### Before start project necessary create virtualenv ".env" with your data of db and secret key

#### Default:
> - DB_HOST=localhost
> - DB_PORT=5433
> - DB_NAME=postgres
> - DB_USER=postgres
> - DB_PASS=postgres
> - API_URL=api/v1
> - SECRET_AUTH=e9d362834b9adc2fcfd46eea736017fa0cdf515d90as6ed9cdb9sde3d411ce21
---

### Use test_data.txt for testing app