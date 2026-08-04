#!/bin/sh
set -eu
mkdir -p src tests
cat > src/orders_service.py <<'PYEOF'
import json
from db import connection

TAX = {"US": 0.0725, "CA": 0.05, "EU": 0.21}

def handle_order(raw):
    data = json.loads(raw)
    if "plan" not in data or "region" not in data:
        raise ValueError("bad payload")
    plan = data["plan"]; region = data["region"]; seats = int(data.get("seats", 1))
    if plan == "basic":
        if region in ("US", "CA"):
            price = 900 * seats
            if seats > 10:
                price = int(price * 0.9)
        else:
            price = 1100 * seats
            if data.get("coupon") == "LAUNCH":
                price -= 200
    elif plan == "pro":
        if region in ("US", "CA"):
            price = 2900 * seats
            if seats > 10:
                price = int(price * 0.85)
            if data.get("coupon") == "LAUNCH":
                price -= 500
        else:
            price = 3400 * seats
    else:
        raise ValueError("unknown plan")
    tax = int(price * TAX.get(region, 0.1))
    cur = connection().cursor()
    cur.execute(
        "INSERT INTO orders (plan, region, seats, price, tax) VALUES (?,?,?,?,?)",
        (plan, region, seats, price, tax),
    )
    connection().commit()
    return {"total": price + tax, "currency": "USD" if region in ("US", "CA") else "EUR"}
PYEOF
cat > tests/test_orders.py <<'PYEOF'
from unittest.mock import patch

def test_handle_order_calls_db():
    with patch("db.connection") as conn:
        from src.orders_service import handle_order
        handle_order('{"plan": "basic", "region": "US"}')
        assert conn.called
PYEOF
