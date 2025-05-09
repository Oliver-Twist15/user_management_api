from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from app.routes import user_routes
from app import auth

load_dotenv()

# FastAPI app initialization
app = FastAPI()

# OAuth2 setup for Swagger UI authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Mount static and templates folders

templates = Jinja2Templates(directory="templates")

# Include user routes
app.include_router(user_routes.router)

# Root endpoint to confirm API is live
@app.get("/")
def root():
    return {"message": "User Management API is running!"}

# Protected route with OAuth2 authentication
@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route", "token": token}

# Endpoint to serve login page
@app.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Endpoint to serve registration page
@app.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
