def check(body, approved=False):
    failed = []

    for key in ("model", "tokens", "latency_ms"):
        if body.get(key) in (None, ""): failed.append(key)
    if int(body.get("tokens") or 0) < 0: failed.append("tokens")
    return {"passed": not failed, "failed": failed, "applied": False, "approved": bool(approved)}
