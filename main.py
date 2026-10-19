import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="device_telemetry.csv")
    args = parser.parse_args()

    csv_path = Path(args.input)
    if not csv_path.is_absolute():
        csv_path = BASE_DIR / csv_path

    if not csv_path.is_file():
        print(f"CSV not found: {csv_path}")
        return 1

    devices = defaultdict(lambda: {
        "total_records": 0,
        "temperature_sum": 0.0,
        "temperature_count": 0,
        "error_count": 0
    })

    with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"device_id", "status", "temperature"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            print("CSV needs device_id, status, temperature columns.")
            return 1

        for row in reader:
            device = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            if not device:
                continue

            item = devices[device]
            item["total_records"] += 1
            if status == "ERROR":
                item["error_count"] += 1

            try:
                temp = float(row.get("temperature", ""))
                if temp == float("inf") or temp == float("-inf") or temp != temp:
                    continue
                item["temperature_sum"] += temp
                item["temperature_count"] += 1
            except (ValueError, TypeError):
                continue

    results = []
    for device, item in sorted(devices.items()):
        count = item["temperature_count"]
        if count == 0:
            continue
        average = item["temperature_sum"] / count
        if average <= 80:
            results.append({
                "device_id": device,
                "total_records": item["total_records"],
                "average_temperature": round(average, 2),
                "error_count": item["error_count"]
            })

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    print(f"{'DEVICE':<12}{'RECORDS':>10}{'AVG TEMP':>14}{'ERRORS':>10}")
    for item in results:
        print(
            f"{item['device_id']:<12}"
            f"{item['total_records']:>10}"
            f"{item['average_temperature']:>14.2f}"
            f"{item['error_count']:>10}"
        )
    print(f"\nJSON saved to output/summary.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
