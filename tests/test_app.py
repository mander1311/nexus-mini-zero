import unittest
import os
import tempfile
from pathlib import Path

from nexus.db import init_db, create_product, get_products, get_product_by_id
from nexus.scoring import calculate_balanced
from nexus.commission import estimate_commission, calculate_projection
from nexus.copywriter import generate_copy


class TestNexusV1(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "nexus.db"
        os.environ["NEXUS_DB_PATH"] = str(self.db_path)
        init_db()

    def tearDown(self):
        self.tempdir.cleanup()
        os.environ.pop("NEXUS_DB_PATH", None)

    def test_db_roundtrip(self):
        created = create_product({
            "name": "Mini ventilador", "marketplace": "Amazon", "price": 149.90,
            "commission_rate": 8, "search_interest": 65, "competition": 35,
            "rating": 4.5, "review_count": 420
        })
        self.assertIsInstance(created["id"], int)
        products = get_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Mini ventilador")
        lookup = get_product_by_id(created["id"])
        self.assertEqual(lookup["commission_estimate"], 11.99)

    def test_commission_formula(self):
        self.assertEqual(estimate_commission(200, 10), 20.0)
        projection = calculate_projection(200, 10, sales=5, conversion_rate=0.1)
        self.assertAlmostEqual(projection["projected_commission"], 10.0)

    def test_balanced_score(self):
        product = {
            "name": "Cabo USB", "marketplace": "Shopee", "price": 89.90,
            "commission_rate": 12, "commission_estimate": 10.79,
            "search_interest": 75, "competition": 38, "rating": 4.7, "review_count": 150
        }
        result = calculate_balanced(product)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertIn("factors", result)

    def test_copywriter_content(self):
        content = generate_copy({
            "name": "Caminha para bebê",
            "marketplace": "Mercado Livre",
            "price": 459.90,
            "commission_rate": 9,
        })
        self.assertIn("Caminha para bebê", content["title"])
        self.assertIn("Aviso", content["affiliate_note"])


if __name__ == "__main__":
    unittest.main()
