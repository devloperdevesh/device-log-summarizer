# AI Prompt Log

## Initial prompt
The exact initial AI prompt used to generate the charting script was not preserved in the available project records. It is not reconstructed or presented as a verbatim prompt.

## Bug in the first attempt
The first-attempt charting bug could not be verified from the available records. No specific bug is claimed here without evidence.

## Follow-up prompt
The exact follow-up prompt used to fix a first-attempt charting bug was not preserved in the available project records. No verbatim follow-up prompt or unverified fix is claimed.

## Verification
Commands run during the current verification:
- `python .\main.py --input ".\demo_device_telemetry.csv" --output ".\output\summary.json"` — completed successfully.
- `python .\plot.py` — chart saved to `output\temperature_chart.png`.
- `python -m pytest -v` — 3 tests passed.
- `python -m py_compile .\cleaning.py .\main.py .\plot.py` — completed successfully.

The demo dataset produced summaries for DEV_A, DEV_B, DEV_C, and DEV_D. DEV_C had an average temperature of 86.50 and was flagged by the greater-than-80 threshold.

Important: `demo_device_telemetry.csv` is demo data, not the original assessment CSV. The final assessment output must be regenerated with the supplied assessment dataset when it becomes available.
