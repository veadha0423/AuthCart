import models
import database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas import CartAdd, ProductCreate
from security import (
    create_access_token,
    get_current_email,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter()


@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "email": new_user.email}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected-route")
def protected_route(email: str = Depends(get_current_email)):
    return {"message": f"Welcome {email}! You have accessed a secure route."}


@router.get("/")
def home():
    return {"message": "Welcome to the AuthCart API! Go to /docs for API documentation."}


@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product created successfully", "product": db_product}


@router.get("/products")
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()


@router.post("/cart")
def add_to_cart(
    item: CartAdd,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == item.product_id,
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = models.CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(cart_item)

    db.commit()
    return {"message": "Item added to cart successfully"}


@router.get("/cart")
def view_cart(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        return {"items": [], "total": 0.0}

    cart_items = []
    total = 0.0
    for item in cart.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product:
            item_total = product.price * item.quantity
            total += item_total
            cart_items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": item_total,
            })

    return {"cart_id": cart.id, "items": cart_items, "total": total}