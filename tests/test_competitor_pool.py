import unittest

from src.competitor_pool import CompetitorPoolService


class CompetitorPoolServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = CompetitorPoolService()

    def test_add_competitor_success(self) -> None:
        item = self.service.add_competitor(
            asin="b012345678",
            brand="Brand A",
            keywords=["wireless charger", "charger", "wireless charger"],
            tier="core",
            tags=["premium", "gift", "gift"],
        )
        self.assertEqual(item.asin, "B012345678")
        self.assertEqual(item.tier, "core")
        self.assertEqual(item.keywords, ["wireless charger", "charger"])
        self.assertEqual(item.tags, ["premium", "gift"])

    def test_add_duplicate_asin_should_fail(self) -> None:
        self.service.add_competitor(asin="B012345678", brand="Brand A")
        with self.assertRaises(ValueError):
            self.service.add_competitor(asin="B012345678", brand="Brand B")

    def test_add_invalid_asin_should_fail(self) -> None:
        with self.assertRaises(ValueError):
            self.service.add_competitor(asin="BAD_ASIN", brand="Brand A")

    def test_update_tier_success(self) -> None:
        self.service.add_competitor(asin="B012345678", brand="Brand A", tier="watch")
        item = self.service.update_tier(asin="B012345678", tier="secondary")
        self.assertEqual(item.tier, "secondary")

    def test_update_tier_not_found_should_fail(self) -> None:
        with self.assertRaises(KeyError):
            self.service.update_tier(asin="B012345678", tier="core")

    def test_list_by_tier(self) -> None:
        self.service.add_competitor(asin="B012345678", brand="Brand A", tier="core")
        self.service.add_competitor(asin="B012345679", brand="Brand B", tier="core")
        self.service.add_competitor(asin="B012345670", brand="Brand C", tier="watch")
        result = self.service.list_by_tier("core")
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
