#!/bin/sh
set -eu
mkdir -p webhooks docs
cat > webhooks/payments.py <<'PYEOF'
import time
from db import orders
from billing import charge_card
from fulfillment import start_fulfillment

def payments_webhook(request):
    event = request.json()  # {"id": "evt_...", "type": "payment.captured", "order_id": ...}
    order = orders.get(event["order_id"])
    charge_card(order.card_token, order.total)   # provider call, no timeout
    order.status = "paid"
    orders.save(order)
    for attempt in range(3):                     # fulfillment is flaky, so retry
        try:
            start_fulfillment(order.id)
            break
        except Exception:
            time.sleep(0)
    return 200
PYEOF
cat > docs/provider.md <<'MDEOF'
# Payment provider webhook notes

Delivery: webhooks are delivered AT LEAST ONCE. Your endpoint may receive
the same event multiple times and must respond 200 within 10 seconds;
otherwise the event is redelivered with backoff for up to 24 hours.
MDEOF
