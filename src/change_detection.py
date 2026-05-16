from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ProductSnapshot:
    asin: str
    price: Optional[float]
    rating: Optional[float]
    review_count: Optional[int]
    title: Optional[str]


@dataclass
class ChangeEvent:
    asin: str
    field: str
    old_value: object
    new_value: object


class ChangeDetectionService:
    TRACKED_FIELDS = ("price", "rating", "review_count", "title")

    def detect_changes(
        self, previous: ProductSnapshot, current: ProductSnapshot
    ) -> List[ChangeEvent]:
        if previous.asin != current.asin:
            raise ValueError("asin mismatch between snapshots")

        events: List[ChangeEvent] = []
        for field in self.TRACKED_FIELDS:
            old_value = getattr(previous, field)
            new_value = getattr(current, field)
            if old_value != new_value:
                events.append(
                    ChangeEvent(
                        asin=current.asin,
                        field=field,
                        old_value=old_value,
                        new_value=new_value,
                    )
                )
        return events

    def summarize_by_field(self, events: List[ChangeEvent]) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for event in events:
            summary[event.field] = summary.get(event.field, 0) + 1
        return summary
