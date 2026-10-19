def clean_sensor_values(values):
    """Convert valid readings to floats, drop invalid/negative values, cap at 500."""
    cleaned = []

    for value in values:
        if value is None:
            continue

        try:
            number = float(value)
        except (ValueError, TypeError):
            continue

        if number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned
