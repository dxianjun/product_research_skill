from dataclasses import dataclass
from typing import Dict, List

from src.change_detection import ChangeEvent
from src.competitor_pool import Competitor


@dataclass
class ProductMetrics:
    asin: str
    price: float
    rating: float
    review_count: int


class DashboardAPI:
    def competitor_overview(self, competitors: List[Competitor]) -> Dict[str, object]:
        by_tier = {"core": 0, "secondary": 0, "watch": 0}
        brands = set()
        for item in competitors:
            if item.tier in by_tier:
                by_tier[item.tier] += 1
            brands.add(item.brand)
        return {
            "total_competitors": len(competitors),
            "tier_distribution": by_tier,
            "brand_count": len(brands),
        }

    def change_timeline(self, events: List[ChangeEvent]) -> List[Dict[str, object]]:
        timeline = []
        for idx, event in enumerate(events):
            timeline.append(
                {
                    "seq": idx + 1,
                    "asin": event.asin,
                    "field": event.field,
                    "old_value": event.old_value,
                    "new_value": event.new_value,
                }
            )
        return timeline

    def gap_analysis(
        self, my_product: ProductMetrics, competitor_products: List[ProductMetrics]
    ) -> Dict[str, object]:
        if not competitor_products:
            return {
                "price_gap_vs_avg": 0.0,
                "rating_gap_vs_avg": 0.0,
                "review_count_gap_vs_avg": 0.0,
            }

        avg_price = sum(x.price for x in competitor_products) / len(competitor_products)
        avg_rating = sum(x.rating for x in competitor_products) / len(competitor_products)
        avg_review_count = sum(x.review_count for x in competitor_products) / len(
            competitor_products
        )

        return {
            "price_gap_vs_avg": round(my_product.price - avg_price, 4),
            "rating_gap_vs_avg": round(my_product.rating - avg_rating, 4),
            "review_count_gap_vs_avg": round(
                my_product.review_count - avg_review_count, 4
            ),
        }
