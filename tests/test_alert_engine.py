import unittest

from src.alert_engine import AlertEngine, AlertRule
from src.change_detection import ChangeEvent


class AlertEngineTests(unittest.TestCase):
    def test_trigger_decrease_rule(self) -> None:
        engine = AlertEngine(
            rules=[
                AlertRule(
                    name="Price Drop High",
                    field="price",
                    threshold=5.0,
                    direction="decrease",
                    level="P1",
                    cooldown_key="price_drop",
                )
            ]
        )
        events = [
            ChangeEvent(
                asin="B012345678",
                field="price",
                old_value=29.99,
                new_value=22.99,
            )
        ]
        alerts = engine.evaluate(events)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].level, "P1")

    def test_not_trigger_when_below_threshold(self) -> None:
        engine = AlertEngine(
            rules=[
                AlertRule(
                    name="Rating Drop",
                    field="rating",
                    threshold=0.5,
                    direction="decrease",
                    level="P2",
                    cooldown_key="rating_drop",
                )
            ]
        )
        events = [
            ChangeEvent(
                asin="B012345678",
                field="rating",
                old_value=4.5,
                new_value=4.2,
            )
        ]
        alerts = engine.evaluate(events)
        self.assertEqual(len(alerts), 0)

    def test_cooldown_dedup_same_key(self) -> None:
        engine = AlertEngine(
            rules=[
                AlertRule(
                    name="Review Surge",
                    field="review_count",
                    threshold=50,
                    direction="increase",
                    level="P3",
                    cooldown_key="review_surge",
                )
            ]
        )
        events = [
            ChangeEvent("B012345678", "review_count", 100, 170),
            ChangeEvent("B012345678", "review_count", 170, 240),
        ]
        alerts = engine.evaluate(events)
        self.assertEqual(len(alerts), 1)

    def test_priority_sorting(self) -> None:
        engine = AlertEngine(
            rules=[
                AlertRule("P3 Rule", "price", 1, "decrease", "P3", "price_minor"),
                AlertRule("P1 Rule", "rating", 0.5, "decrease", "P1", "rating_major"),
            ]
        )
        events = [
            ChangeEvent("B012345678", "price", 20, 18),
            ChangeEvent("B012345678", "rating", 4.8, 4.0),
        ]
        alerts = engine.evaluate(events)
        self.assertEqual(len(alerts), 2)
        self.assertEqual(alerts[0].level, "P1")
        self.assertEqual(alerts[1].level, "P3")

    def test_invalid_rule_direction_should_fail(self) -> None:
        engine = AlertEngine(
            rules=[
                AlertRule("Bad Direction", "price", 1, "down", "P2", "x"),
            ]
        )
        events = [ChangeEvent("B012345678", "price", 20, 18)]
        with self.assertRaises(ValueError):
            engine.evaluate(events)


if __name__ == "__main__":
    unittest.main()
