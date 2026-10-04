from fastapi.testclient import TestClient
from plat.main import app
client = TestClient(app)

def test_pass_fail():
    assert client.post("/check", json={'model': 'local-small', 'tokens': 42, 'latency_ms': 12, 'cost_usd': 0.0, 'quality': 0.8}).json()["passed"] is True
    bad = client.post("/check", json={'model': 'local-small', 'latency_ms': 12}).json()
    assert bad["passed"] is False
    assert "tokens" in bad["failed"]
