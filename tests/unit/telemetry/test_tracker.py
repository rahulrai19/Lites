import pytest
from app.telemetry.tracker import TelemetryTracker

@pytest.mark.asyncio
async def test_telemetry_tracker_records_metrics():
    tracker = TelemetryTracker()
    
    await tracker.record_request()
    await tracker.record_request()
    
    await tracker.record_exact_cache_hit()
    await tracker.record_semantic_cache_hit()
    
    await tracker.record_rule_savings(100)
    await tracker.record_ai_savings(50)
    
    await tracker.record_overhead(25)
    await tracker.record_overhead(35)
    
    metrics = tracker.get_metrics()
    
    assert metrics.total_requests == 2
    assert metrics.exact_cache_hits == 1
    assert metrics.semantic_cache_hits == 1
    assert metrics.tokens_saved_by_rules == 100
    assert metrics.tokens_saved_by_ai == 50
    assert metrics.total_optimization_overhead_ms == 60

@pytest.mark.asyncio
async def test_telemetry_ignores_negative_savings():
    tracker = TelemetryTracker()
    
    # Negative savings means the AI made the prompt longer!
    # Lites correctly rejects this, so savings should be 0.
    await tracker.record_ai_savings(-10)
    
    metrics = tracker.get_metrics()
    assert metrics.tokens_saved_by_ai == 0
