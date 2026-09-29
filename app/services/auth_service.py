from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def register_user(db: Session, email: str, password: str):
        existing_user = UserRepository.get_by_email(db, email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = UserRepository.create(db, email, get_password_hash(password))
        return {"message": "User registered successfully", "email": user.email}

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
