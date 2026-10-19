from cleaning import clean_sensor_values


def test_converts_values_and_caps_large_readings():
    assert clean_sensor_values([10, "20.5", 700]) == [10.0, 20.5, 500.0]


def test_drops_none_invalid_and_negative_values():
    assert clean_sensor_values([None, "bad", -5, "12"]) == [12.0]


def test_empty_and_all_invalid_inputs():
    assert clean_sensor_values([]) == []
    assert clean_sensor_values([None, "bad", -1]) == []
