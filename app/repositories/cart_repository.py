from sqlalchemy.orm import Session

from app import models


class CartRepository:
    @staticmethod
    def get_by_user_id(db: Session, user_id: int):
        return db.query(models.Cart).filter(models.Cart.user_id == user_id).first()

    @staticmethod
    def create(db: Session, user_id: int):
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def get_item(db: Session, cart_id: int, product_id: int):
        return db.query(models.CartItem).filter(
            models.CartItem.cart_id == cart_id,
            models.CartItem.product_id == product_id,
        ).first()

    @staticmethod
    def create_item(db: Session, cart_id: int, product_id: int, quantity: int):
        item = models.CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
