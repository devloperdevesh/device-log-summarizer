import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "output" / "summary.json"
OUTPUT_FILE = BASE_DIR / "output" / "temperature_chart.png"


def main():
    if not INPUT_FILE.is_file():
        print("Error: output/summary.json not found. Run main.py first.")
        return 1

    try:
        data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Expected a JSON list")

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Each item must be an object")
            if "device_id" not in item or "average_temperature" not in item:
                raise ValueError("Required chart fields are missing")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error loading JSON: {exc}")
        return 1

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not data:
        print("No device data available to plot.")
        return 0

    devices = [str(item["device_id"]) for item in data]
    averages = [float(item["average_temperature"]) for item in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(devices, averages)

    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.margins(y=0.15)
    fig.tight_layout()

    try:
        fig.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")
    except OSError as exc:
        print(f"Error saving chart: {exc}")
        return 1
    finally:
        plt.close(fig)

    print(f"Chart saved to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
