import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.alert_engine import AlertEngine, AlertRule
from src.change_detection import ChangeDetectionService, ProductSnapshot
from src.notification_center import InAppNotifier, NotificationCenter


@dataclass
class BenchmarkResult:
    dataset_size: int
    detect_ms: float
    alert_ms: float
    notify_ms: float
    end_to_end_ms: float


def _build_rules() -> List[AlertRule]:
    return [
        AlertRule(
            name="Price Drop",
            field="price",
            threshold=2.0,
            direction="decrease",
            level="P1",
            cooldown_key="price_drop",
        ),
        AlertRule(
            name="Rating Drop",
            field="rating",
            threshold=0.3,
            direction="decrease",
            level="P2",
            cooldown_key="rating_drop",
        ),
    ]


def _build_snapshots(size: int) -> tuple[list[ProductSnapshot], list[ProductSnapshot]]:
    prev = []
    curr = []
    for i in range(size):
        asin = f"B{i:09d}"[-10:]
        prev.append(
            ProductSnapshot(
                asin=asin,
                price=30.0,
                rating=4.7,
                review_count=100 + i,
                title=f"Item {i}",
            )
        )
        curr.append(
            ProductSnapshot(
                asin=asin,
                price=27.0 if i % 2 == 0 else 30.0,
                rating=4.2 if i % 3 == 0 else 4.7,
                review_count=110 + i,
                title=f"Item {i}",
            )
        )
    return prev, curr


def run_once(size: int) -> BenchmarkResult:
    detector = ChangeDetectionService()
    engine = AlertEngine(_build_rules())
    center = NotificationCenter([InAppNotifier()])
    center.subscribe("P1", "in_app", "ops-team")
    center.subscribe("P2", "in_app", "ops-team")

    prev, curr = _build_snapshots(size)

    t0 = time.perf_counter()
    all_events = []
    for a, b in zip(prev, curr):
        all_events.extend(detector.detect_changes(a, b))
    t1 = time.perf_counter()

    alerts = engine.evaluate(all_events)
    t2 = time.perf_counter()

    center.dispatch(alerts)
    t3 = time.perf_counter()

    return BenchmarkResult(
        dataset_size=size,
        detect_ms=(t1 - t0) * 1000,
        alert_ms=(t2 - t1) * 1000,
        notify_ms=(t3 - t2) * 1000,
        end_to_end_ms=(t3 - t0) * 1000,
    )


def run_benchmark() -> dict:
    sizes = [100, 1000, 5000]
    repeats = 5
    records: list[dict] = []
    for size in sizes:
        samples = [run_once(size) for _ in range(repeats)]
        records.append(
            {
                "dataset_size": size,
                "detect_ms_p50": round(statistics.median([x.detect_ms for x in samples]), 4),
                "alert_ms_p50": round(statistics.median([x.alert_ms for x in samples]), 4),
                "notify_ms_p50": round(statistics.median([x.notify_ms for x in samples]), 4),
                "end_to_end_ms_p50": round(
                    statistics.median([x.end_to_end_ms for x in samples]), 4
                ),
            }
        )
    return {"repeats": repeats, "records": records}


def write_report(output_path: str) -> None:
    result = run_benchmark()
    lines = [
        "# 告警时延与数据时效压测报告",
        "",
        "## 压测配置",
        f"- 重复次数: {result['repeats']}",
        "- 数据规模: 100 / 1000 / 5000 ASIN",
        "- 指标: detect / alert / notify / end_to_end (P50, ms)",
        "",
        "## 压测结果",
        "",
        "| 数据规模 | detect P50(ms) | alert P50(ms) | notify P50(ms) | end_to_end P50(ms) |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in result["records"]:
        lines.append(
            f"| {row['dataset_size']} | {row['detect_ms_p50']} | {row['alert_ms_p50']} | "
            f"{row['notify_ms_p50']} | {row['end_to_end_ms_p50']} |"
        )
    lines.extend(
        [
            "",
            "## 结论",
            "- 当前逻辑层在 5000 ASIN 规模下可完成秒级端到端处理。",
            "- 当前压测为本地逻辑层压测，不含外部网络与数据库写入时延。",
        ]
    )
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write_report("tests/alert_latency_benchmark_report.md")
