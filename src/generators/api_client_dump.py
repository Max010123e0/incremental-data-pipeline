import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from typing import Optional 

def validate_iso(ts: str) -> str:
    datetime.fromisoformat(ts)
    return ts

def output_path(root: Path, since_iso: str) -> Path:
    dt = datetime.fromisoformat(since_iso)
    return root / "api" / f"{dt.year:04d}" / f"{dt.month:02d}" / f"{dt.day:02d}" / f"{dt.hour:02d}" / "events.jsonl"

def fetch_events(base_url: str, since_iso: str, limit: int, seed: Optional[int]):  
    params = {"since": since_iso, "limit": str(limit)}
    if seed is not None:
        params["seed"] = str(seed)
    url = f"{base_url}?{urlencode(params)}"
    with urlopen(url) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload["since"], payload["events"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base_url", default="http://127.0.0.1:8000/events")
    p.add_argument("--since", required=True, help="e.g. 2026-01-05T15:00:00")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--out_root", default="landing")
    args = p.parse_args()

    since_iso = validate_iso(args.since)
    source_since, events = fetch_events(args.base_url, since_iso, args.limit, args.seed)

    out = output_path(Path(args.out_root), since_iso)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    print(f"Wrote {len(events)} events to {out}")
    print(f"API returned since={source_since}")

if __name__ == "__main__":
    main()
