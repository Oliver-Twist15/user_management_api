from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.routes import user_routes
from app import auth

# OAuth2 Password Bearer setup for Swagger UI Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Root endpoint to confirm API is live
@app.get("/")
def root():
    return {"message": "User Management API is running!"}

# Include user routes
app.include_router(user_routes.router)

# Add this authorization flow to ensure Swagger UI shows the "Authorize" button
@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route", "token": token}
