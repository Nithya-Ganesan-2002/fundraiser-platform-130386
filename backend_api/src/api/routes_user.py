from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.api import schemas, models, database, auth

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

# PUBLIC_INTERFACE
@router.post("/register", response_model=schemas.UserInDB, summary="User registration")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new application user."""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")
    db_user = models.User(
        email=user.email,
        hashed_password=auth.get_password_hash(user.password),
        name=user.name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# PUBLIC_INTERFACE
@router.post("/token", summary="User login", response_model=dict)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Dependency for protected endpoints
# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Get current user from JWT token."""
    payload = auth.decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials.")
    user = db.query(models.User).filter(models.User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# PUBLIC_INTERFACE
@router.get("/me", response_model=schemas.UserInDB, summary="Current user account")
def read_current_user(current_user: models.User = Depends(get_current_user)):
    """Get current user's info."""
    return current_user
