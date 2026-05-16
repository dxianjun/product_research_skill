import unittest

from src.change_detection import ChangeDetectionService, ProductSnapshot


class ChangeDetectionServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ChangeDetectionService()

    def test_detect_no_changes(self) -> None:
        before = ProductSnapshot("B012345678", 19.99, 4.5, 100, "Title A")
        after = ProductSnapshot("B012345678", 19.99, 4.5, 100, "Title A")
        events = self.service.detect_changes(before, after)
        self.assertEqual(len(events), 0)

    def test_detect_price_and_rating_changes(self) -> None:
        before = ProductSnapshot("B012345678", 19.99, 4.5, 100, "Title A")
        after = ProductSnapshot("B012345678", 17.99, 4.2, 100, "Title A")
        events = self.service.detect_changes(before, after)
        fields = sorted([e.field for e in events])
        self.assertEqual(fields, ["price", "rating"])

    def test_detect_asin_mismatch_should_fail(self) -> None:
        before = ProductSnapshot("B012345678", 19.99, 4.5, 100, "Title A")
        after = ProductSnapshot("B012345679", 17.99, 4.2, 100, "Title A")
        with self.assertRaises(ValueError):
            self.service.detect_changes(before, after)

    def test_summarize_by_field(self) -> None:
        before = ProductSnapshot("B012345678", 19.99, 4.5, 100, "Old")
        after = ProductSnapshot("B012345678", 17.99, 4.2, 120, "New")
        events = self.service.detect_changes(before, after)
        summary = self.service.summarize_by_field(events)
        self.assertEqual(summary.get("price"), 1)
        self.assertEqual(summary.get("rating"), 1)
        self.assertEqual(summary.get("review_count"), 1)
        self.assertEqual(summary.get("title"), 1)


if __name__ == "__main__":
    unittest.main()
