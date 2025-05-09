from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app import schemas, models, auth
from app.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# OAuth2PasswordBearer for Swagger UI Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register route
@router.post("/register", response_model=schemas.UserOut)
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.hash_password(password)
    new_user = models.User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login route
@router.post("/login")
def login(
    username: str = Form(...),  # 👈 change to username
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == username).first()  # 👈 use username as email
    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "user_name": user.name
    }

# Get user profile route
@router.get("/profile/{id}", response_model=schemas.UserOut)
def get_profile(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user profile route
@router.put("/profile/{id}", response_model=schemas.UserOut)
def update_profile(
    id: int,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.email = email
    user.password = auth.hash_password(password)
    db.commit()
    db.refresh(user)
    return user
