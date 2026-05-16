import unittest

from src.change_detection import ChangeEvent
from src.competitor_pool import Competitor
from src.dashboard_api import DashboardAPI, ProductMetrics


class DashboardAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = DashboardAPI()

    def test_competitor_overview(self) -> None:
        competitors = [
            Competitor(asin="B012345678", brand="A", tier="core"),
            Competitor(asin="B012345679", brand="A", tier="watch"),
            Competitor(asin="B012345670", brand="B", tier="secondary"),
        ]
        result = self.api.competitor_overview(competitors)
        self.assertEqual(result["total_competitors"], 3)
        self.assertEqual(result["tier_distribution"]["core"], 1)
        self.assertEqual(result["brand_count"], 2)

    def test_change_timeline(self) -> None:
        events = [
            ChangeEvent("B012345678", "price", 20, 18),
            ChangeEvent("B012345678", "rating", 4.8, 4.6),
        ]
        timeline = self.api.change_timeline(events)
        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0]["seq"], 1)
        self.assertEqual(timeline[1]["field"], "rating")

    def test_gap_analysis(self) -> None:
        mine = ProductMetrics("MYASIN0001", 19.99, 4.6, 120)
        peers = [
            ProductMetrics("B012345678", 17.99, 4.4, 100),
            ProductMetrics("B012345679", 21.99, 4.8, 140),
        ]
        result = self.api.gap_analysis(mine, peers)
        self.assertAlmostEqual(result["price_gap_vs_avg"], 0.0, places=4)
        self.assertAlmostEqual(result["rating_gap_vs_avg"], 0.0, places=4)
        self.assertAlmostEqual(result["review_count_gap_vs_avg"], 0.0, places=4)

    def test_gap_analysis_empty_peer(self) -> None:
        mine = ProductMetrics("MYASIN0001", 19.99, 4.6, 120)
        result = self.api.gap_analysis(mine, [])
        self.assertEqual(result["price_gap_vs_avg"], 0.0)
        self.assertEqual(result["rating_gap_vs_avg"], 0.0)
        self.assertEqual(result["review_count_gap_vs_avg"], 0.0)


if __name__ == "__main__":
    unittest.main()
