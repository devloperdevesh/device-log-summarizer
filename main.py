import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def summarize_csv(csv_path):
    devices = defaultdict(
        lambda: {"record_count": 0, "temperatures": [], "error_count": 0}
    )

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"device_id", "status", "temperature"}

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain device_id, status, temperature columns."
            )

        for row in reader:
            device_id = (row.get("device_id") or "").strip()
            if not device_id:
                continue

            item = devices[device_id]
            item["record_count"] += 1

            if (row.get("status") or "").strip().upper() == "ERROR":
                item["error_count"] += 1

            try:
                temperature = float(row["temperature"])
                item["temperatures"].append(temperature)
            except (ValueError, TypeError, KeyError):
                pass

    summaries = []

    for device_id, item in sorted(devices.items()):
        temperatures = item["temperatures"]
        average = (
            round(sum(temperatures) / len(temperatures), 2)
            if temperatures else None
        )

        summaries.append({
            "device_id": device_id,
            "record_count": item["record_count"],
            "average_temperature": average,
            "error_count": item["error_count"],
        })

    high_temperature_devices = [
        item for item in summaries
        if item["average_temperature"] is not None
        and item["average_temperature"] > 80
    ]

    return {
        "devices": summaries,
        "high_temperature_devices": high_temperature_devices,
    }


def print_table(report):
    headers = ["DEVICE", "RECORDS", "AVG TEMP", "ERRORS"]
    rows = []

    for item in report["devices"]:
        average = item["average_temperature"]
        rows.append([
            item["device_id"],
            str(item["record_count"]),
            f"{average:.2f}" if average is not None else "N/A",
            str(item["error_count"]),
        ])

    widths = [
        max([len(headers[i])] + [len(row[i]) for row in rows])
        for i in range(len(headers))
    ]

    print(" | ".join(headers[i].ljust(widths[i]) for i in range(4)))
    print("-+-".join("-" * width for width in widths))

    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(4)))

    print("\nDevices with average temperature > 80:")
    flagged = report["high_temperature_devices"]

    if not flagged:
        print("None")
    else:
        for item in flagged:
            print(f"- {item['device_id']}: {item['average_temperature']:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Summarize device telemetry from CSV."
    )
    parser.add_argument(
        "--input",
        default="device_telemetry.csv",
        help="Input CSV path",
    )
    parser.add_argument(
        "--output",
        default="output/summary.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    csv_path = Path(args.input)
    output_path = Path(args.output)

    if not csv_path.is_file():
        parser.error(f"CSV not found: {csv_path}")

    try:
        report = summarize_csv(csv_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )
    except (OSError, csv.Error, ValueError) as exc:
        parser.error(str(exc))

    print_table(report)
    print(f"\nJSON saved to: {output_path}")


if __name__ == "__main__":
    main()
