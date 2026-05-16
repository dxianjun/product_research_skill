import unittest

from src.market_monitor import (
    CategoryPoint,
    KeywordPoint,
    MarketMonitorService,
    ProductLaunch,
)


class MarketMonitorServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = MarketMonitorService()

    def test_keyword_trend_summary(self) -> None:
        points = [
            KeywordPoint("wireless charger", 1000, 0.8),
            KeywordPoint("fast charger", 800, 0.6),
            KeywordPoint("magnetic charger", 1200, 0.7),
        ]
        result = self.service.keyword_trend_summary(points)
        self.assertEqual(result["keywords"], 3)
        self.assertAlmostEqual(result["avg_search_volume"], 1000.0, places=4)
        self.assertEqual(result["top_keywords"][0], "magnetic charger")

    def test_keyword_trend_summary_empty(self) -> None:
        result = self.service.keyword_trend_summary([])
        self.assertEqual(result["keywords"], 0)
        self.assertEqual(result["top_keywords"], [])

    def test_category_trend_summary(self) -> None:
        points = [
            CategoryPoint("Chargers", 100.0, "2026-05-01"),
            CategoryPoint("Chargers", 112.0, "2026-05-08"),
            CategoryPoint("Cables", 80.0, "2026-05-01"),
            CategoryPoint("Cables", 78.0, "2026-05-08"),
        ]
        result = self.service.category_trend_summary(points)
        self.assertEqual(result["categories"], 2)
        self.assertAlmostEqual(result["trend_delta"], 10.0, places=4)

    def test_launch_activity_summary(self) -> None:
        launches = [
            ProductLaunch("BrandA", "B012345678", "2026-05-01"),
            ProductLaunch("BrandA", "B012345679", "2026-05-02"),
            ProductLaunch("BrandB", "B012345670", "2026-05-03"),
        ]
        result = self.service.launch_activity_summary(launches)
        self.assertEqual(result["total_launches"], 3)
        self.assertEqual(result["active_brands"], 2)
        self.assertEqual(result["top_brands"][0], "BrandA")


if __name__ == "__main__":
    unittest.main()
