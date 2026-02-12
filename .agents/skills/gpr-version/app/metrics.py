from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    "opsboard_http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

http_request_latency_seconds = Histogram(
    "opsboard_http_request_latency_seconds",
    "HTTP request latency",
    ["method", "path"],
)

domain_events_total = Counter(
    "opsboard_domain_events_total",
    "Domain events emitted",
    ["action"],
)
