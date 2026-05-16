import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.alert_engine import Alert, AlertEngine, AlertRule
from src.change_detection import ChangeDetectionService, ProductSnapshot
from src.notification_center import NotificationCenter


@dataclass
class ExternalProductRecord:
    asin: str
    price: float
    rating: float
    review_count: int
    title: str


class ExternalDataAdapter:
    """
    Adapter for external feed exports (json file based).
    Expected schema:
    {
      "source": "amazon_feed",
      "items": [
        {"asin": "...", "price": 19.99, "rating": 4.5, "review_count": 123, "title": "..."}
      ]
    }
    """

    def load_records(self, file_path: str) -> List[ExternalProductRecord]:
        payload = json.loads(Path(file_path).read_text(encoding="utf-8"))
        items = payload.get("items", [])
        records: List[ExternalProductRecord] = []
        for item in items:
            records.append(
                ExternalProductRecord(
                    asin=str(item["asin"]).strip().upper(),
                    price=float(item["price"]),
                    rating=float(item["rating"]),
                    review_count=int(item["review_count"]),
                    title=str(item["title"]).strip(),
                )
            )
        return records


class ExternalIntegrationAcceptanceService:
    def __init__(
        self,
        adapter: ExternalDataAdapter,
        detector: ChangeDetectionService,
        alert_engine: AlertEngine,
        notifier_center: NotificationCenter,
    ) -> None:
        self.adapter = adapter
        self.detector = detector
        self.alert_engine = alert_engine
        self.notifier_center = notifier_center

    @staticmethod
    def _to_snapshot(record: ExternalProductRecord) -> ProductSnapshot:
        return ProductSnapshot(
            asin=record.asin,
            price=record.price,
            rating=record.rating,
            review_count=record.review_count,
            title=record.title,
        )

    def run_acceptance(self, previous_feed: str, current_feed: str) -> dict:
        prev_records = self.adapter.load_records(previous_feed)
        curr_records = self.adapter.load_records(current_feed)
        prev_map = {x.asin: x for x in prev_records}
        curr_map = {x.asin: x for x in curr_records}

        total_events = 0
        all_alerts: List[Alert] = []
        for asin, curr in curr_map.items():
            if asin not in prev_map:
                continue
            events = self.detector.detect_changes(
                self._to_snapshot(prev_map[asin]), self._to_snapshot(curr)
            )
            total_events += len(events)
            all_alerts.extend(self.alert_engine.evaluate(events))

        notifications = self.notifier_center.dispatch(all_alerts)
        return {
            "records_previous": len(prev_records),
            "records_current": len(curr_records),
            "change_events": total_events,
            "alerts": len(all_alerts),
            "notifications": len(notifications),
        }


def default_alert_rules() -> List[AlertRule]:
    return [
        AlertRule(
            name="External Price Drop",
            field="price",
            threshold=3.0,
            direction="decrease",
            level="P1",
            cooldown_key="ext_price_drop",
        ),
        AlertRule(
            name="External Rating Drop",
            field="rating",
            threshold=0.4,
            direction="decrease",
            level="P2",
            cooldown_key="ext_rating_drop",
        ),
    ]
