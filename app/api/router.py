from fastapi import APIRouter

from app.api.endpoints import auth, cart, products

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(cart.router, tags=["cart"])


@api_router.get("/", tags=["health"])
def home():
    return {"message": "Welcome to the AuthCart API! Go to /docs for API documentation."}