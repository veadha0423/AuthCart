from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone

import models, database
from pydantic import BaseModel

# Pydantic schemas for request validation
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int

class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1

# Secret key to sign JWT tokens (In production, load this from environment variables)
SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize FastAPI app
app = FastAPI(title="AuthCart API")

# Initialize database tables on startup
models.Base.metadata.create_all(bind=database.engine)

# Password hashing setup using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Helper functions for security
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
# Helper to get the currently authenticated user object from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# --- ROUTES ---

@app.post("/register")
def register_user(email: str, password: str, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and save user
    hashed_pwd = get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "email": new_user.email}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Authenticate user credentials
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-route")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return {"message": f"Welcome {email}! You have accessed a secure route."}
@app.get("/")
def home():
    return {"message": "Welcome to the AuthCart API! Go to /docs for API documentation."}
# --- PRODUCT ROUTES ---

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product created successfully", "product": db_product}

@app.get("/products")
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()


# --- CART ROUTES (With IDOR Protection) ---

@app.post("/cart")
def add_to_cart(item: CartAdd, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # 1. Ensure product exists
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Get or create cart strictly bound to the authenticated user ID
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # 3. Check if item already exists in cart, update quantity if so
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id, 
        models.CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = models.CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    db.commit()
    return {"message": "Item added to cart successfully"}

@app.get("/cart")
def view_cart(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # IDOR Prevention: We fetch ONLY the cart belonging to current_user.id from the token, 
    # completely ignoring any user-supplied IDs in parameters.
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        return {"items": [], "total": 0.0}

    # Format cart items with details
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
                "subtotal": item_total
            })

    return {"cart_id": cart.id, "items": cart_items, "total": total}