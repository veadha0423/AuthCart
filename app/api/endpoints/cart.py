from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas import CartAdd
from app.services.cart_service import CartService

router = APIRouter()


@router.post("/cart")
def add_to_cart(
    item: CartAdd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return CartService.add_item_to_cart(db, current_user, item)


@router.get("/cart")
def view_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return CartService.get_cart_summary(db, current_user)