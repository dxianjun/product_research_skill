from dataclasses import dataclass
from typing import Dict, List, Protocol, Set, Tuple

from src.alert_engine import Alert


@dataclass(frozen=True)
class NotificationRecord:
    channel: str
    target: str
    alert_level: str
    alert_rule: str
    message: str


class Notifier(Protocol):
    channel_name: str

    def send(self, target: str, alert: Alert) -> NotificationRecord:
        ...


class InAppNotifier:
    channel_name = "in_app"

    def send(self, target: str, alert: Alert) -> NotificationRecord:
        return NotificationRecord(
            channel=self.channel_name,
            target=target,
            alert_level=alert.level,
            alert_rule=alert.rule_name,
            message=alert.message,
        )


class EmailNotifier:
    channel_name = "email"

    def send(self, target: str, alert: Alert) -> NotificationRecord:
        return NotificationRecord(
            channel=self.channel_name,
            target=target,
            alert_level=alert.level,
            alert_rule=alert.rule_name,
            message=alert.message,
        )


class NotificationCenter:
    def __init__(self, notifiers: List[Notifier]) -> None:
        self._notifier_map: Dict[str, Notifier] = {
            notifier.channel_name: notifier for notifier in notifiers
        }
        self._subscriptions: Dict[str, Dict[str, List[str]]] = {}
        self._sent_keys: Set[Tuple[str, str, str, str]] = set()

    def subscribe(self, alert_level: str, channel: str, target: str) -> None:
        if channel not in self._notifier_map:
            raise ValueError("unsupported channel")
        by_channel = self._subscriptions.setdefault(alert_level, {})
        targets = by_channel.setdefault(channel, [])
        if target not in targets:
            targets.append(target)

    def dispatch(self, alerts: List[Alert]) -> List[NotificationRecord]:
        records: List[NotificationRecord] = []
        for alert in alerts:
            if alert.level not in self._subscriptions:
                continue
            channel_map = self._subscriptions[alert.level]
            for channel, targets in channel_map.items():
                notifier = self._notifier_map[channel]
                for target in targets:
                    key = (alert.asin, alert.rule_name, channel, target)
                    # Ensure idempotency for the same alert + channel + target.
                    if key in self._sent_keys:
                        continue
                    self._sent_keys.add(key)
                    records.append(notifier.send(target, alert))
        return records
