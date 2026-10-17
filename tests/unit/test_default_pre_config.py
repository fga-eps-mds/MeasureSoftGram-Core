from staticfiles import DEFAULT_PRE_CONFIG


def _characteristics():
    return {c["key"]: c for c in DEFAULT_PRE_CONFIG["characteristics"]}


def test_default_pre_config_does_not_include_performance_efficiency():
    assert "performance_efficiency" not in _characteristics()


def test_default_pre_config_characteristics_and_weights():
    weights = {key: c["weight"] for key, c in _characteristics().items()}

    assert weights == {
        "reliability": 34,
        "maintainability": 33,
        "functional_suitability": 33,
    }


def test_default_pre_config_weights_sum_100_at_every_level():
    characteristics = DEFAULT_PRE_CONFIG["characteristics"]
    assert sum(c["weight"] for c in characteristics) == 100

    for characteristic in characteristics:
        subcharacteristics = characteristic["subcharacteristics"]
        assert sum(s["weight"] for s in subcharacteristics) == 100

        for subcharacteristic in subcharacteristics:
            assert sum(m["weight"] for m in subcharacteristic["measures"]) == 100
