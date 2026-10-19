# Device Log Summarizer

Python CLI tool for summarizing device telemetry from CSV data.

## Requirements
- Python 3.10+
- matplotlib

## Input
Place the assessment-provided `device_telemetry.csv` in this directory.
It must contain `device_id`, `status`, and `temperature` columns.

## Setup (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run
```powershell
python cleaning.py
python main.py
python plot.py
```

`main.py` writes `output/summary.json`.
`plot.py` writes `output/temperature_chart.png`.

Devices with average temperatures above 80.0 are excluded.
Invalid temperatures are ignored for the average and reported.
Rows with a missing device ID are skipped.

## Tests
Complete Section 1 independently, then run:
```powershell
python -m unittest discover -s tests -v
```
