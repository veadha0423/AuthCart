from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models
from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas import ProductCreate
from app.services.product_service import ProductService

router = APIRouter()


@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return ProductService.create_product(db, product)


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return ProductService.get_products(db)