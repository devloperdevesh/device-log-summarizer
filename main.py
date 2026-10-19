import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "device_telemetry.csv"
OUTPUT_DIR = BASE_DIR / "output"
JSON_FILE = OUTPUT_DIR / "summary.json"


def main():
    if not CSV_FILE.is_file():
        print(f"Error: CSV file not found: {CSV_FILE}")
        print("Place the provided device_telemetry.csv in the project folder.")
        return 1

    devices = defaultdict(
        lambda: {"total_records": 0, "temperature_sum": 0.0,
                 "temperature_count": 0, "error_count": 0}
    )

    try:
        with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            required = {"device_id", "status", "temperature"}

            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                print("Error: CSV must contain device_id, status, temperature.")
                return 1

            for line_number, row in enumerate(reader, start=2):
                device_id = (row.get("device_id") or "").strip()
                status = (row.get("status") or "").strip().upper()

                if not device_id:
                    print(f"Warning: Skipping row {line_number}: missing device_id.")
                    continue

                item = devices[device_id]
                item["total_records"] += 1

                if status == "ERROR":
                    item["error_count"] += 1

                try:
                    temperature = float(row.get("temperature", ""))
                    if not __import__("math").isfinite(temperature):
                        raise ValueError("Temperature must be finite")
                    item["temperature_sum"] += temperature
                    item["temperature_count"] += 1
                except (ValueError, TypeError):
                    print(f"Warning: Invalid temperature at row {line_number}.")

    except (OSError, csv.Error, UnicodeError) as exc:
        print(f"Error reading CSV: {exc}")
        return 1

    results = []
    for device_id, item in sorted(devices.items()):
        count = item["temperature_count"]
        if count == 0:
            print(f"Warning: Excluding {device_id}: no valid temperatures.")
            continue

        average = item["temperature_sum"] / count

        if average > 80.0:
            continue

        results.append({
            "device_id": device_id,
            "total_records": item["total_records"],
            "average_temperature": round(average, 2),
            "error_count": item["error_count"],
        })

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        JSON_FILE.write_text(
            json.dumps(results, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        print(f"Error writing JSON: {exc}")
        return 1

    print(f"\n{'DEVICE':<16}{'RECORDS':>10}{'AVG TEMP':>14}{'ERRORS':>10}")
    print("-" * 50)
    for item in results:
        print(
            f"{item['device_id']:<16}"
            f"{item['total_records']:>10}"
            f"{item['average_temperature']:>14.2f}"
            f"{item['error_count']:>10}"
        )

    print(f"\nSaved {len(results)} device summaries to {JSON_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
