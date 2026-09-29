from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import get_current_email
from app.db.database import get_db
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    return AuthService.register_user(db, email, password)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login_user(db, form_data.username, form_data.password)


@router.get("/protected-route")
def protected_route(email: str = Depends(get_current_email)):
    return {"message": f"Welcome {email}! You have accessed a secure route."}