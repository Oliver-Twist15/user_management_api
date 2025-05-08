from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app import schemas, models, auth
from app.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# OAuth2PasswordBearer for Swagger UI Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile/{id}", response_model=schemas.UserOut)
def get_profile(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile/{id}", response_model=schemas.UserOut)
def update_profile(id: int, user_update: schemas.UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update.name
    user.email = user_update.email
    user.password = auth.hash_password(user_update.password)
    db.commit()
    db.refresh(user)
    return user
