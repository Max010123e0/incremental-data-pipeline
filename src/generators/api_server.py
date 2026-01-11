import random
import uuid
from datetime import datetime, timedelta, timezone

from flask import Flask, request, jsonify

app = Flask(__name__)

EVENT_TYPES = ["view", "click", "purchase", "signup"]

def parse_since(since_str: str) -> datetime:
    dt = datetime.fromisoformat(since_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

@app.get("/events")
def get_events():
    """
    Simulated API:
    - /events?since=<iso>&limit=<int>&seed=<int>
    - returns events with event_time >= since
    """
    since_str = request.args.get("since")
    if not since_str:
        return jsonify({"error": "missing required query param: since"}), 400

    limit = int(request.args.get("limit", "200"))
    seed = request.args.get("seed")
    seed = int(seed) if seed is not None else None

    rng = random.Random(seed)
    since = parse_since(since_str)

    window_end = since + timedelta(minutes=10)

    events = []
    for _ in range(limit):
        offset_seconds = rng.randint(0, int((window_end - since).total_seconds()))
        event_time = since + timedelta(seconds=offset_seconds)

        events.append(
            {
                "event_id": str(uuid.uuid4()),
                "event_time": event_time.isoformat(),
                "user_id": rng.randint(1, 50_000),
                "event_type": rng.choice(EVENT_TYPES),
                "value": rng.randint(1, 100),
            }
        )

    return jsonify({"since": since.isoformat(), "count": len(events), "events": events})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
