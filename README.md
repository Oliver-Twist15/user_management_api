# User Management API (FastAPI + PostgreSQL)

## 🛠 Tech Stack
- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- JWT (python-jose)  
- Bcrypt  
- Pydantic  

---

## ⚙️ Setup Instructions

1. Create a PostgreSQL database named `user_db`.
2. Create a `.env` file in the root directory with the following content:
DATABASE_URL=postgresql://username:password@localhost:5432/user_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256

- Install dependencies:
pip install -r requirements.txt

- Start the server:
uvicorn main:app --reload


---

##  API Endpoints

| Method | Endpoint         | Description         |
|--------|------------------|---------------------|
| POST   | `/register`      | Register a new user |
| POST   | `/login`         | Login & get token   |
| GET    | `/profile/{id}`  | Get user profile    |
| PUT    | `/profile/{id}`  | Update user profile |

---

##  Authentication

- A JWT token is returned upon successful login.
- For secure routes, add this header:
Authorization: Bearer <your_token>


---

##  How to Run Locally

```bash
git clone https://github.com/Oliver-Twist15/user_management_api.git
cd user_management_api
uvicorn main:app --reload
Visit the API documentation at:
http://localhost:8000/docs
