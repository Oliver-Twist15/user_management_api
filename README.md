# User Management API (FastAPI + PostgreSQL)

## 🚀 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (python-jose)
- Bcrypt
- Pydantic

## ⚙️ Setup Instructions

1. Create a PostgreSQL DB called `user_db`
2. Set your DB credentials in `.env`
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the API:
```
uvicorn app.main:app --reload
```

## 📌 API Endpoints

| Method | Endpoint         | Description         |
|--------|------------------|---------------------|
| POST   | `/register`      | Register a new user |
| POST   | `/login`         | Login & get token   |
| GET    | `/profile/{id}`  | Get user profile    |
| PUT    | `/profile/{id}`  | Update user profile |
