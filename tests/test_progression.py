from plat.progression import llmops

def test_llmops_trace_cost():
    out = llmops({"prompt_tokens": 100, "completion_tokens": 50, "latency_ms": 80, "quality": 0.9})
    assert out["tokens"] == 150
    assert "cost" in out["trace"]
    assert out["cost_usd"] > 0

