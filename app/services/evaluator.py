from typing import Dict, Optional


class Evaluator:
    """
    Lightweight in-memory evaluator for QA metrics.

    Tracks:
    - total number of queries
    - average latency
    - average token usage

    Intended for developer-facing instrumentation, not model benchmarking.
    """

    def __init__(self):
        self.total_queries = 0
        self.total_latency_ms = 0.0
        self.total_tokens = 0

    def record(self, latency_ms: float, usage: Optional[Dict] = None) -> None:
        self.total_queries += 1
        self.total_latency_ms += latency_ms

        if usage and "total_tokens" in usage:
            self.total_tokens += usage["total_tokens"]

    def summary(self) -> Dict[str, float]:
        if self.total_queries == 0:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0.0,
                "avg_tokens": 0.0,
            }

        return {
            "total_queries": self.total_queries,
            "avg_latency_ms": self.total_latency_ms / self.total_queries,
            "avg_tokens": self.total_tokens / self.total_queries,
        }
