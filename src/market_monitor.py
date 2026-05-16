from dataclasses import dataclass
from typing import Dict, List


@dataclass
class KeywordPoint:
    keyword: str
    search_volume: int
    competition_score: float


@dataclass
class CategoryPoint:
    category: str
    sales_index: float
    period: str


@dataclass
class ProductLaunch:
    brand: str
    asin: str
    launch_date: str


class MarketMonitorService:
    def keyword_trend_summary(self, points: List[KeywordPoint]) -> Dict[str, object]:
        if not points:
            return {
                "keywords": 0,
                "avg_search_volume": 0.0,
                "avg_competition_score": 0.0,
                "top_keywords": [],
            }
        avg_sv = sum(p.search_volume for p in points) / len(points)
        avg_comp = sum(p.competition_score for p in points) / len(points)
        top = sorted(points, key=lambda x: x.search_volume, reverse=True)[:3]
        return {
            "keywords": len(points),
            "avg_search_volume": round(avg_sv, 4),
            "avg_competition_score": round(avg_comp, 4),
            "top_keywords": [p.keyword for p in top],
        }

    def category_trend_summary(self, points: List[CategoryPoint]) -> Dict[str, object]:
        if not points:
            return {"categories": 0, "trend_delta": 0.0}
        by_category: Dict[str, List[CategoryPoint]] = {}
        for point in points:
            by_category.setdefault(point.category, []).append(point)

        trend_delta_sum = 0.0
        for items in by_category.values():
            if len(items) < 2:
                continue
            # Use first and last as simple trend proxy by time sequence input.
            trend_delta_sum += items[-1].sales_index - items[0].sales_index
        return {
            "categories": len(by_category),
            "trend_delta": round(trend_delta_sum, 4),
        }

    def launch_activity_summary(self, launches: List[ProductLaunch]) -> Dict[str, object]:
        brands: Dict[str, int] = {}
        for launch in launches:
            brands[launch.brand] = brands.get(launch.brand, 0) + 1
        top_brands = sorted(brands.items(), key=lambda kv: kv[1], reverse=True)[:3]
        return {
            "total_launches": len(launches),
            "active_brands": len(brands),
            "top_brands": [b for b, _ in top_brands],
        }
