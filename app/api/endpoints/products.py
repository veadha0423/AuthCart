from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models
from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas import ProductCreate

router = APIRouter()


@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product created successfully", "product": db_product}


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()