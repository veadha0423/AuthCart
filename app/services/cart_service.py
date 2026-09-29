from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository


class CartService:
    @staticmethod
    def add_item_to_cart(db: Session, current_user: models.User, item):
        product = ProductRepository.get_by_id(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        cart = CartRepository.get_by_user_id(db, current_user.id)
        if not cart:
            cart = CartRepository.create(db, current_user.id)

        cart_item = CartRepository.get_item(db, cart.id, item.product_id)
        if cart_item:
            cart_item.quantity += item.quantity
        else:
            CartRepository.create_item(db, cart.id, item.product_id, item.quantity)

        db.commit()
        return {"message": "Item added to cart successfully"}

    @staticmethod
    def get_cart_summary(db: Session, current_user: models.User):
        cart = CartRepository.get_by_user_id(db, current_user.id)
        if not cart:
            return {"items": [], "total": 0.0}

        cart_items = []
        total = 0.0
        for item in cart.items:
            product = ProductRepository.get_by_id(db, item.product_id)
            if product:
                item_total = product.price * item.quantity
                total += item_total
                cart_items.append(
                    {
                        "product_id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": item.quantity,
                        "subtotal": item_total,
                    }
                )

        return {"cart_id": cart.id, "items": cart_items, "total": total}
