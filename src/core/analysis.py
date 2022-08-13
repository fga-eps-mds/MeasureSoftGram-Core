from typing import Dict, List, Tuple

import pandas as pd

from src.core.agregation import aggregation_operation
from src.core.weighting import weighting_operation
from src.util.constants import MEASURES_INTERPRETATION_MAPPING


def resolve_level(level_dict: dict, sublevel: dict, sublevel_key: str) -> Tuple[dict, dict]:
    aggregated_level, all_weighted_values = {}, {}
    for key, value in level_dict.items():
        level_items = value[sublevel_key]
        level_weights = value["weights"]

        weights_list, values_list = [], []
        for item in level_items:
            weights_list.append(level_weights[item])
            values_list.append(sublevel[item])

        weighted_items = weighting_operation(values_list, weights_list)
        aggregated_value = aggregation_operation(weighted_items, weights_list)

        weighted_items_dict = {item: weighted_items[idx] for idx, item in enumerate(level_items)}

        aggregated_level[key] = aggregated_value
        all_weighted_values[key] = weighted_items_dict

    return aggregated_level, all_weighted_values


def make_analysis(measures: dict, subcharacteristics: dict, characteristics: dict):

    aggregated_scs, weighted_measures_per_scs = resolve_level(
        subcharacteristics, measures, "measures"
    )

    aggregated_characteristics, weighted_scs_per_c = resolve_level(
        characteristics, aggregated_scs, "subcharacteristics"
    )

    characteristics_weights = {}

    for key, value in characteristics.items():
        characteristics_weights[key] = value["weight"]

    aggregated_sqc, weighted_c = resolve_level(
        {
            "sqc": {
                "weights": characteristics_weights,
                "characteristics": list(aggregated_characteristics.keys()),
            },
        },
        aggregated_characteristics,
        "characteristics",
    )

    return (
        aggregated_sqc,
        aggregated_scs,
        aggregated_characteristics,
        weighted_measures_per_scs,
        weighted_scs_per_c,
        weighted_c,
    )


def calculate_measures(dataframe: pd.DataFrame, measures: List[str]) -> Dict[str, float]:
    combined_measures = {}
    for measure in measures:
        combined_measures[measure] = MEASURES_INTERPRETATION_MAPPING[measure]["interpretation_function"](dataframe)

    return combined_measures


def calculate_aggregated_value(values_list: List[float], weights_list: List[float]) -> float:
    weighted_items = weighting_operation(values_list, weights_list)
    aggregated_value = aggregation_operation(weighted_items, weights_list)
    return aggregated_value
