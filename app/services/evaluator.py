class Evaluator:
    """
    Simple in-memory evaluator for QA performance metrics.
    """

    def __init__(self):
        self.total_queries = 0
        self.total_latency_ms = 0.0
        self.total_tokens = 0

    def record(self, latency_ms: float, usage: dict):
        self.total_queries += 1
        self.total_latency_ms += latency_ms

        if usage and "total_tokens" in usage:
            self.total_tokens += usage["total_tokens"]

    def summary(self):
        if self.total_queries == 0:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0,
                "avg_tokens": 0,
            }

        return {
            "total_queries": self.total_queries,
            "avg_latency_ms": self.total_latency_ms / self.total_queries,
            "avg_tokens": self.total_tokens / self.total_queries,
        }
