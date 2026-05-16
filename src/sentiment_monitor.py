from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ReviewRecord:
    rating: float
    sentiment: str  # "positive" | "neutral" | "negative"
    text: str


class SentimentMonitorService:
    TOPIC_KEYWORDS = {
        "quality": ["quality", "broken", "durable", "cheap"],
        "logistics": ["delivery", "shipping", "arrived", "late"],
        "packaging": ["package", "packaging", "box", "seal"],
        "function": ["work", "charge", "speed", "compatible"],
        "support": ["support", "refund", "service", "return"],
    }

    def topic_cluster(self, reviews: List[ReviewRecord]) -> Dict[str, int]:
        result: Dict[str, int] = {k: 0 for k in self.TOPIC_KEYWORDS.keys()}
        for review in reviews:
            text = review.text.lower()
            for topic, words in self.TOPIC_KEYWORDS.items():
                if any(word in text for word in words):
                    result[topic] += 1
        return result

    def sentiment_summary(self, reviews: List[ReviewRecord]) -> Dict[str, float]:
        total = len(reviews)
        if total == 0:
            return {"positive": 0.0, "neutral": 0.0, "negative": 0.0}
        counts = {"positive": 0, "neutral": 0, "negative": 0}
        for review in reviews:
            if review.sentiment in counts:
                counts[review.sentiment] += 1
        return {
            "positive": round(counts["positive"] / total, 4),
            "neutral": round(counts["neutral"] / total, 4),
            "negative": round(counts["negative"] / total, 4),
        }

    def risk_events(self, reviews: List[ReviewRecord]) -> List[str]:
        events: List[str] = []
        summary = self.sentiment_summary(reviews)
        avg_rating = 0.0
        if reviews:
            avg_rating = sum(r.rating for r in reviews) / len(reviews)

        if summary["negative"] >= 0.4:
            events.append("negative sentiment surge")
        if avg_rating <= 3.5 and len(reviews) >= 5:
            events.append("rating drop risk")
        return events
