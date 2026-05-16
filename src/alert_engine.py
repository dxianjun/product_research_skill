from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.change_detection import ChangeEvent

ALERT_LEVELS = ("P1", "P2", "P3")


@dataclass
class AlertRule:
    name: str
    field: str
    threshold: float
    direction: str  # "increase" | "decrease"
    level: str
    cooldown_key: str


@dataclass
class Alert:
    asin: str
    level: str
    rule_name: str
    field: str
    old_value: object
    new_value: object
    message: str


class AlertEngine:
    def __init__(self, rules: Optional[List[AlertRule]] = None) -> None:
        self.rules = rules or []
        self._cooldown_seen: Dict[Tuple[str, str], bool] = {}

    def evaluate(self, events: List[ChangeEvent]) -> List[Alert]:
        alerts: List[Alert] = []
        for event in events:
            for rule in self.rules:
                if rule.field != event.field:
                    continue
                if self._is_triggered(rule, event):
                    key = (event.asin, rule.cooldown_key)
                    # De-dup same asin + cooldown key in one evaluation window.
                    if self._cooldown_seen.get(key):
                        continue
                    self._cooldown_seen[key] = True
                    alerts.append(
                        Alert(
                            asin=event.asin,
                            level=rule.level,
                            rule_name=rule.name,
                            field=event.field,
                            old_value=event.old_value,
                            new_value=event.new_value,
                            message=self._build_message(rule, event),
                        )
                    )
        return sorted(alerts, key=lambda a: ALERT_LEVELS.index(a.level))

    @staticmethod
    def _build_message(rule: AlertRule, event: ChangeEvent) -> str:
        return (
            f"[{rule.level}] {rule.name}: {event.field} changed "
            f"from {event.old_value} to {event.new_value}"
        )

    @staticmethod
    def _number(value: object) -> Optional[float]:
        if isinstance(value, (int, float)):
            return float(value)
        return None

    def _is_triggered(self, rule: AlertRule, event: ChangeEvent) -> bool:
        if rule.level not in ALERT_LEVELS:
            raise ValueError("invalid alert level")
        old_num = self._number(event.old_value)
        new_num = self._number(event.new_value)
        if old_num is None or new_num is None:
            return False

        delta = new_num - old_num
        if rule.direction == "increase":
            return delta >= rule.threshold
        if rule.direction == "decrease":
            return (-delta) >= rule.threshold
        raise ValueError("invalid rule direction")
