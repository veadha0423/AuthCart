import unittest

from app.main import app
from app.db.database import Base

from app.services.auth_service import AuthService
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository


class ApiRouteTests(unittest.TestCase):
    def test_expected_routes_are_registered(self):
        expected_paths = {
            "/",
            "/register",
            "/login",
            "/protected-route",
            "/products",
            "/cart",
        }

        self.assertTrue(expected_paths.issubset(app.openapi()["paths"]))
        self.assertSetEqual(
            {"users", "products", "carts", "cart_items"},
            set(Base.metadata.tables),
        )

    def test_service_and_repository_layers_are_present(self):
        self.assertTrue(callable(AuthService.register_user))
        self.assertTrue(callable(AuthService.login_user))
        self.assertTrue(callable(ProductService.create_product))
        self.assertTrue(callable(ProductService.get_products))
        self.assertTrue(callable(CartService.add_item_to_cart))
        self.assertTrue(callable(CartService.get_cart_summary))
        self.assertTrue(callable(UserRepository.get_by_email))
        self.assertTrue(callable(ProductRepository.get_by_id))
        self.assertTrue(callable(CartRepository.get_by_user_id))


if __name__ == "__main__":
    unittest.main()