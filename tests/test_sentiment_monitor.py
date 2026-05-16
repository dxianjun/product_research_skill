import unittest

from src.sentiment_monitor import ReviewRecord, SentimentMonitorService


class SentimentMonitorServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SentimentMonitorService()

    def test_topic_cluster(self) -> None:
        reviews = [
            ReviewRecord(5, "positive", "Great quality and durable build."),
            ReviewRecord(2, "negative", "Late delivery and broken package."),
            ReviewRecord(3, "neutral", "Support suggested return process."),
        ]
        result = self.service.topic_cluster(reviews)
        self.assertGreaterEqual(result["quality"], 1)
        self.assertGreaterEqual(result["logistics"], 1)
        self.assertGreaterEqual(result["support"], 1)

    def test_sentiment_summary(self) -> None:
        reviews = [
            ReviewRecord(5, "positive", "good"),
            ReviewRecord(4, "positive", "good"),
            ReviewRecord(3, "neutral", "ok"),
            ReviewRecord(1, "negative", "bad"),
        ]
        result = self.service.sentiment_summary(reviews)
        self.assertAlmostEqual(result["positive"], 0.5, places=4)
        self.assertAlmostEqual(result["neutral"], 0.25, places=4)
        self.assertAlmostEqual(result["negative"], 0.25, places=4)

    def test_sentiment_summary_empty(self) -> None:
        result = self.service.sentiment_summary([])
        self.assertEqual(result["positive"], 0.0)
        self.assertEqual(result["negative"], 0.0)

    def test_risk_events(self) -> None:
        reviews = [
            ReviewRecord(2, "negative", "bad quality"),
            ReviewRecord(2, "negative", "broken"),
            ReviewRecord(3, "negative", "not good"),
            ReviewRecord(3, "neutral", "ok"),
            ReviewRecord(2, "negative", "late shipping"),
        ]
        events = self.service.risk_events(reviews)
        self.assertIn("negative sentiment surge", events)
        self.assertIn("rating drop risk", events)


if __name__ == "__main__":
    unittest.main()
