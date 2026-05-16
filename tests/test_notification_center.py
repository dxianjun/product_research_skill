import unittest

from src.alert_engine import Alert
from src.notification_center import EmailNotifier, InAppNotifier, NotificationCenter


class NotificationCenterTests(unittest.TestCase):
    def _sample_alert(self, level: str = "P1") -> Alert:
        return Alert(
            asin="B012345678",
            level=level,
            rule_name="Price Drop High",
            field="price",
            old_value=29.99,
            new_value=22.99,
            message="[P1] Price Drop High: price changed from 29.99 to 22.99",
        )

    def test_subscribe_and_dispatch_single_channel(self) -> None:
        center = NotificationCenter([InAppNotifier(), EmailNotifier()])
        center.subscribe("P1", "in_app", "ops-team")
        records = center.dispatch([self._sample_alert("P1")])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].channel, "in_app")
        self.assertEqual(records[0].target, "ops-team")

    def test_dispatch_multi_channel(self) -> None:
        center = NotificationCenter([InAppNotifier(), EmailNotifier()])
        center.subscribe("P1", "in_app", "ops-team")
        center.subscribe("P1", "email", "ops@example.com")
        records = center.dispatch([self._sample_alert("P1")])
        channels = sorted([r.channel for r in records])
        self.assertEqual(channels, ["email", "in_app"])

    def test_dispatch_without_subscription(self) -> None:
        center = NotificationCenter([InAppNotifier(), EmailNotifier()])
        records = center.dispatch([self._sample_alert("P2")])
        self.assertEqual(len(records), 0)

    def test_idempotent_dispatch(self) -> None:
        center = NotificationCenter([InAppNotifier(), EmailNotifier()])
        center.subscribe("P1", "in_app", "ops-team")
        alert = self._sample_alert("P1")
        first = center.dispatch([alert])
        second = center.dispatch([alert])
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 0)

    def test_subscribe_unsupported_channel_should_fail(self) -> None:
        center = NotificationCenter([InAppNotifier()])
        with self.assertRaises(ValueError):
            center.subscribe("P1", "sms", "10086")


if __name__ == "__main__":
    unittest.main()
