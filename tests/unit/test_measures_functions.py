"""
Regression tests for default thresholds of aggregated normalized measures.

These tests pin the relationship between the canonical thresholds declared in
``DEFAULT_PRE_CONFIG`` and the defaults hardcoded in the measure functions in
``src/core/aggregated_normalized_measures.py``. Any divergence between them is a
bug — the function defaults should match the canonical configuration, otherwise
calling the function without a config silently produces a different
normalization than the production pipeline.
"""

import inspect

from core.aggregated_normalized_measures import run_time_measure
from staticfiles.default_pre_config import DEFAULT_PRE_CONFIG

# Limite canônico do response_time. A característica performance_efficiency
# saiu do DEFAULT_PRE_CONFIG (decisão do P.O., US01.01), mas a medida continua
# suportada pelo Core e calculada pela CLI a partir dos arquivos perf-eff.
RESPONSE_TIME_MAX_THRESHOLD = 0.66


def _measure_keys(config):
    return {
        measure["key"]
        for characteristic in config["characteristics"]
        for subcharacteristic in characteristic["subcharacteristics"]
        for measure in subcharacteristic["measures"]
    }


def test_run_time_measure_default_max_threshold_matches_response_time_config():
    """
    Issue #14: run_time_measure tinha max_threshold padrão 0.33 fixo no código,
    divergente do limite canônico 0.66 do response_time. O padrão da função
    precisa ser igual ao limite canônico; senão, chamadas diretas (sem config)
    normalizam de forma diferente do pipeline que passa o limite da config.
    """
    signature = inspect.signature(run_time_measure)
    function_default = signature.parameters["max_threshold"].default

    assert function_default == RESPONSE_TIME_MAX_THRESHOLD, (
        f"run_time_measure default max_threshold={function_default} diverges "
        f"from the canonical response_time max_threshold="
        f"{RESPONSE_TIME_MAX_THRESHOLD}"
    )


def test_response_time_is_not_in_default_pre_config():
    assert "response_time" not in _measure_keys(DEFAULT_PRE_CONFIG)
