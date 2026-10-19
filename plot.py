import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def create_temperature_chart(json_path, output_path):
    json_path = Path(json_path)
    output_path = Path(output_path)

    if not json_path.is_file():
        raise FileNotFoundError(f"Summary JSON not found: {json_path}")

    report = json.loads(json_path.read_text(encoding="utf-8"))
    devices = report.get("devices", [])

    valid_devices = [
        item for item in devices
        if item.get("average_temperature") is not None
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))

    if valid_devices:
        names = [item["device_id"] for item in valid_devices]
        averages = [item["average_temperature"] for item in valid_devices]

        bars = ax.bar(names, averages)
        ax.bar_label(bars, fmt="%.2f", padding=3)
        ax.set_xlabel("Device ID")
        ax.set_ylabel("Average temperature")
        ax.set_title("Average Temperature by Device")
        ax.margins(y=0.15)
    else:
        ax.text(
            0.5, 0.5, "No valid temperature data",
            ha="center", va="center",
            transform=ax.transAxes,
        )
        ax.set_title("Average Temperature by Device")
        ax.set_axis_off()

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Plot device temperatures from summary JSON."
    )
    parser.add_argument("--input", default="output/summary.json")
    parser.add_argument("--output", default="output/temperature_chart.png")
    args = parser.parse_args()

    try:
        create_temperature_chart(args.input, args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
