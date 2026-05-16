import unittest

from src.alert_engine import AlertEngine
from src.change_detection import ChangeDetectionService
from src.external_data_integration import (
    ExternalDataAdapter,
    ExternalIntegrationAcceptanceService,
    default_alert_rules,
)
from src.notification_center import InAppNotifier, NotificationCenter


class ExternalDataIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        adapter = ExternalDataAdapter()
        detector = ChangeDetectionService()
        engine = AlertEngine(default_alert_rules())
        notifier = NotificationCenter([InAppNotifier()])
        notifier.subscribe("P1", "in_app", "ops-team")
        notifier.subscribe("P2", "in_app", "ops-team")
        self.service = ExternalIntegrationAcceptanceService(
            adapter=adapter,
            detector=detector,
            alert_engine=engine,
            notifier_center=notifier,
        )

    def test_external_feed_acceptance_flow(self) -> None:
        summary = self.service.run_acceptance(
            "data_sources/amazon_feed_previous.json",
            "data_sources/amazon_feed_current.json",
        )
        self.assertEqual(summary["records_previous"], 2)
        self.assertEqual(summary["records_current"], 2)
        self.assertGreaterEqual(summary["change_events"], 3)
        self.assertEqual(summary["alerts"], 2)
        self.assertEqual(summary["notifications"], 2)


if __name__ == "__main__":
    unittest.main()
