import unittest

from src.alert_engine import Alert
from src.report_generator import (
    DailyReportInput,
    ReportGenerator,
    WeeklyReportInput,
)


class ReportGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = ReportGenerator()

    def _sample_alerts(self):
        return [
            Alert(
                asin="B012345678",
                level="P1",
                rule_name="Price Drop High",
                field="price",
                old_value=29.99,
                new_value=22.99,
                message="[P1] Price Drop High: price changed from 29.99 to 22.99",
            ),
            Alert(
                asin="B012345679",
                level="P2",
                rule_name="Rating Drop",
                field="rating",
                old_value=4.8,
                new_value=4.2,
                message="[P2] Rating Drop: rating changed from 4.8 to 4.2",
            ),
        ]

    def test_generate_daily_markdown_with_data(self) -> None:
        content = self.generator.generate_daily_markdown(
            DailyReportInput(
                date="2026-05-16",
                key_changes=["Competitor A price down", "Competitor B new reviews up"],
                alerts=self._sample_alerts(),
                actions=["Adjust coupon strategy", "Review listing copy"],
            )
        )
        self.assertIn("# Daily Report (2026-05-16)", content)
        self.assertIn("- P1: 1", content)
        self.assertIn("- P2: 1", content)
        self.assertIn("## Priority Actions", content)

    def test_generate_daily_markdown_empty_fallback(self) -> None:
        content = self.generator.generate_daily_markdown(
            DailyReportInput(
                date="2026-05-16",
                key_changes=[],
                alerts=[],
                actions=[],
            )
        )
        self.assertIn("- No key changes", content)
        self.assertIn("- No alerts", content)
        self.assertIn("- No actions", content)

    def test_generate_weekly_markdown(self) -> None:
        content = self.generator.generate_weekly_markdown(
            WeeklyReportInput(
                week_range="2026-W20",
                strategy_changes=["Competitor A expanded keyword set"],
                market_signals=["Demand up for wireless charger"],
                sentiment_summary=["Negative sentiment stable"],
                next_week_actions=["Prepare new A+ assets"],
            )
        )
        self.assertIn("# Weekly Report (2026-W20)", content)
        self.assertIn("## Strategy Changes", content)
        self.assertIn("- Prepare new A+ assets", content)


if __name__ == "__main__":
    unittest.main()
