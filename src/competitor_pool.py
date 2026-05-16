import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

VALID_TIERS = {"core", "secondary", "watch"}


@dataclass
class Competitor:
    asin: str
    brand: str
    keywords: List[str] = field(default_factory=list)
    tier: str = "watch"
    tags: List[str] = field(default_factory=list)


class CompetitorPoolService:
    def __init__(self) -> None:
        self._items: Dict[str, Competitor] = {}

    @staticmethod
    def _normalize_asin(asin: str) -> str:
        value = asin.strip().upper()
        if not re.fullmatch(r"[A-Z0-9]{10}", value):
            raise ValueError("asin must be 10 alphanumeric characters")
        return value

    @staticmethod
    def _normalize_tier(tier: str) -> str:
        value = tier.strip().lower()
        if value not in VALID_TIERS:
            raise ValueError("tier must be one of: core, secondary, watch")
        return value

    @staticmethod
    def _normalize_list(values: Optional[List[str]]) -> List[str]:
        if not values:
            return []
        result: List[str] = []
        for value in values:
            item = value.strip()
            if item and item not in result:
                result.append(item)
        return result

    def add_competitor(
        self,
        asin: str,
        brand: str,
        keywords: Optional[List[str]] = None,
        tier: str = "watch",
        tags: Optional[List[str]] = None,
    ) -> Competitor:
        normalized_asin = self._normalize_asin(asin)
        if normalized_asin in self._items:
            raise ValueError("asin already exists in competitor pool")

        brand_value = brand.strip()
        if not brand_value:
            raise ValueError("brand is required")

        competitor = Competitor(
            asin=normalized_asin,
            brand=brand_value,
            keywords=self._normalize_list(keywords),
            tier=self._normalize_tier(tier),
            tags=self._normalize_list(tags),
        )
        self._items[normalized_asin] = competitor
        return competitor

    def update_tier(self, asin: str, tier: str) -> Competitor:
        normalized_asin = self._normalize_asin(asin)
        if normalized_asin not in self._items:
            raise KeyError("asin not found")
        self._items[normalized_asin].tier = self._normalize_tier(tier)
        return self._items[normalized_asin]

    def list_by_tier(self, tier: str) -> List[Competitor]:
        normalized_tier = self._normalize_tier(tier)
        return [item for item in self._items.values() if item.tier == normalized_tier]

    def get(self, asin: str) -> Competitor:
        normalized_asin = self._normalize_asin(asin)
        if normalized_asin not in self._items:
            raise KeyError("asin not found")
        return self._items[normalized_asin]

    def count(self) -> int:
        return len(self._items)
