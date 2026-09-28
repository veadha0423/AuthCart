import unittest

from app.main import app
from app.db.database import Base


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


if __name__ == "__main__":
    unittest.main()