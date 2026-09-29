from sqlalchemy.orm import Session

from app import models


class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def create(db: Session, email: str, hashed_password: str):
        user = models.User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
