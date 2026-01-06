import argparse
import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

EVENT_TYPES = ["view", "click", "purchase", "signup"]


def parse_hour(hour_str: str) -> datetime:
    """
    Accepts: 'YYYY-MM-DDTHH' or 'YYYY-MM-DDTHH:00'
    Example: '2026-01-05T15'
    Returns a datetime rounded down to the hour.
    """
    dt = datetime.fromisoformat(hour_str)
    return dt.replace(minute=0, second=0, microsecond=0)


def output_path(root: Path, hour: datetime) -> Path:
    # landing/csv/YYYY/MM/DD/HH/events.csv
    return (
        root
        / "csv"
        / f"{hour.year:04d}"
        / f"{hour.month:02d}"
        / f"{hour.day:02d}"
        / f"{hour.hour:02d}"
        / "events.csv"
    )


def generate_rows(hour: datetime, n: int, seed: Optional[int] = None):
    rng = random.Random(seed)
    rows = []

    for _ in range(n):
        # Random timestamp within the hour
        event_time = hour + timedelta(seconds=rng.randint(0, 3599))

        rows.append(
            {
                "event_id": str(uuid.uuid4()),
                "event_time": event_time.isoformat(),
                "user_id": rng.randint(1, 50_000),
                "event_type": rng.choice(EVENT_TYPES),
                "value": rng.randint(1, 100),
            }
        )

    return rows


def write_csv(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["event_id", "event_time", "user_id", "event_type", "value"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate hourly CSV events.")
    parser.add_argument("--hour", required=True, help="e.g. 2026-01-05T15")
    parser.add_argument("--n", type=int, default=5000, help="number of rows to generate")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    parser.add_argument("--out_root", default="landing", help="output root folder (default: landing)")
    args = parser.parse_args()

    hour = parse_hour(args.hour)
    out = output_path(Path(args.out_root), hour)
    rows = generate_rows(hour, args.n, args.seed)
    write_csv(out, rows)

    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
