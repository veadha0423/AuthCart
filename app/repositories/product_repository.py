from sqlalchemy.orm import Session

from app import models


class ProductRepository:
    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(models.Product).filter(models.Product.id == product_id).first()

    @staticmethod
    def create(db: Session, product_data):
        product = models.Product(**product_data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def list(db: Session):
        return db.query(models.Product).all()
