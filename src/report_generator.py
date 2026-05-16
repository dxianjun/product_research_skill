from dataclasses import dataclass
from typing import Dict, List

from src.alert_engine import Alert


@dataclass
class DailyReportInput:
    date: str
    key_changes: List[str]
    alerts: List[Alert]
    actions: List[str]


@dataclass
class WeeklyReportInput:
    week_range: str
    strategy_changes: List[str]
    market_signals: List[str]
    sentiment_summary: List[str]
    next_week_actions: List[str]


class ReportGenerator:
    def _group_alerts(self, alerts: List[Alert]) -> Dict[str, int]:
        summary: Dict[str, int] = {"P1": 0, "P2": 0, "P3": 0}
        for alert in alerts:
            if alert.level in summary:
                summary[alert.level] += 1
        return summary

    @staticmethod
    def _lines(items: List[str], empty_text: str) -> str:
        if not items:
            return f"- {empty_text}"
        return "\n".join([f"- {item}" for item in items])

    def generate_daily_markdown(self, data: DailyReportInput) -> str:
        alert_summary = self._group_alerts(data.alerts)
        alert_lines = self._lines([a.message for a in data.alerts], "No alerts")
        return (
            f"# Daily Report ({data.date})\n\n"
            f"## Key Changes\n{self._lines(data.key_changes, 'No key changes')}\n\n"
            "## Alert Summary\n"
            f"- P1: {alert_summary['P1']}\n"
            f"- P2: {alert_summary['P2']}\n"
            f"- P3: {alert_summary['P3']}\n\n"
            f"## Alerts\n{alert_lines}\n\n"
            f"## Priority Actions\n{self._lines(data.actions, 'No actions')}\n"
        )

    def generate_weekly_markdown(self, data: WeeklyReportInput) -> str:
        strategy = self._lines(data.strategy_changes, "No strategy changes")
        market = self._lines(data.market_signals, "No market signals")
        sentiment = self._lines(data.sentiment_summary, "No sentiment updates")
        actions = self._lines(data.next_week_actions, "No actions planned")
        return (
            f"# Weekly Report ({data.week_range})\n\n"
            f"## Strategy Changes\n{strategy}\n\n"
            f"## Market Signals\n{market}\n\n"
            f"## Sentiment Summary\n{sentiment}\n\n"
            f"## Next Week Actions\n{actions}\n"
        )
