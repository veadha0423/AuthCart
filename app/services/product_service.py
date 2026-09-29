from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository


class ProductService:
    @staticmethod
    def create_product(db: Session, product_data):
        product = ProductRepository.create(db, product_data)
        return {"message": "Product created successfully", "product": product}

    @staticmethod
    def get_products(db: Session):
        return ProductRepository.list(db)
