"""
Contract test for the technical_debt_ratio measure.

It pins the data shapes exchanged between the repositories involved in
issue #7 of 2026.2-MeasureSoftGram-Service, so Action, Parser, CLI and Service
can be developed in parallel against the same expectations:

1. Action/Parser: SonarQube ``/api/measures/component_tree`` returns
   ``sqale_debt_ratio`` (a percentage, as a string) for every ``FIL`` component.
2. CLI -> Core: only ``FIL`` values are sent, as a list of floats under the
   metric key ``sqale_debt_ratio`` (``TRK``, ``DIR`` and ``UTS`` are ignored).
3. Core -> CLI/Service: ``{"key": "technical_debt_ratio", "value": <0..1>}``.
"""

import json
from pathlib import Path

import pytest

from resources.analysis import calculate_measures
from staticfiles.default_pre_config import DEFAULT_PRE_CONFIG

SONAR_COMPONENT_TREE = Path(__file__).parent / (
    "data/technical_debt_ratio_sonar_component_tree.json"
)


def _file_values(component_tree, metric):
    return [
        float(measure["value"])
        for component in component_tree["components"]
        if component["qualifier"] == "FIL"
        for measure in component["measures"]
        if measure["metric"] == metric
    ]


def test_technical_debt_ratio_contract_from_sonar_component_tree():
    component_tree = json.loads(SONAR_COMPONENT_TREE.read_text())

    sqale_debt_ratio = _file_values(component_tree, "sqale_debt_ratio")
    assert sqale_debt_ratio == [0.0, 8.3, 4.0, 32.5]

    result = calculate_measures(
        extracted_measures={
            "measures": [
                {
                    "key": "technical_debt_ratio",
                    "metrics": [{"key": "sqale_debt_ratio", "value": sqale_debt_ratio}],
                }
            ]
        },
        config=DEFAULT_PRE_CONFIG,
    )

    # (1 + (1 - 8.3 / 20) + (1 - 4.0 / 20) + 0) / 4 = 0.59625
    assert result == {
        "measures": [{"key": "technical_debt_ratio", "value": pytest.approx(0.59625)}]
    }
