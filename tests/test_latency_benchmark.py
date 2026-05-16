import unittest

from scripts.latency_benchmark import run_benchmark


class LatencyBenchmarkTests(unittest.TestCase):
    def test_benchmark_output_shape(self) -> None:
        result = run_benchmark()
        self.assertIn("repeats", result)
        self.assertIn("records", result)
        self.assertEqual(len(result["records"]), 3)
        for row in result["records"]:
            self.assertIn("dataset_size", row)
            self.assertIn("end_to_end_ms_p50", row)
            self.assertGreaterEqual(row["end_to_end_ms_p50"], 0.0)


if __name__ == "__main__":
    unittest.main()
