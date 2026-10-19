# AI Prompt Log

## Initial prompt
The charting task was to write a Python script that loads the
Section 2 JSON output and generates a matplotlib bar chart comparing
average temperature per device.

Note: The exact original prompt wording was not preserved, so this
is a summary of the request, not a verbatim transcript.

## First-attempt bug
The available records do not preserve the first chart attempt or a
verified formatting bug. I have not attributed an unverified bug to
the first attempt.

## Follow-up prompt
The exact original follow-up prompt was not preserved. The chart
script was reviewed for a title, axis labels, readable value labels,
layout spacing, and reliable image saving.

## Verification
- `python -m pytest -v` — 3 tests passed.
- `python -m py_compile .\cleaning.py .\main.py .\plot.py` — passed.
- `python .\main.py --input .\demo_device_telemetry.csv --output .\output\summary.json` — succeeded with demo data.
- `python .\plot.py` — generated `output\temperature_chart.png`.

Important: The demo CSV is not the original assessment dataset.
Regenerate and verify the final output using the supplied
`device_telemetry.csv` before claiming validation against that dataset.
