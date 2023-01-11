from typing import Dict, List, Tuple

import pandas as pd

from core.agregation import aggregation_operation
from core.weighting import weighting_operation
from util.constants import MEASURES_INTERPRETATION_MAPPING


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


def calculate_sqc(pre_config: Dict, metrics: List[Dict]) -> float:
    """
    Calculates the SQC.

    This function calculates the SQC given a pre_config and the metrics values.
    For this it implements the DFS algorithm (`calculate_entity_item`) iterating
    through all items in the pre_config and calculating their aggregated value.
    """
    pre_config = update_pre_config_dict(pre_config)

    def calculate_entity_item(item: Dict) -> None:
        entity_name = item["entity"]
        sub_entity_name = item["sub_entity"]

        # Base Case - Calculate the measure value using its interpretation function
        if entity_name == "measures":
            item["value"] = calculate_measure(
                measure_key=item["key"],
                metrics=metrics
            )
            return

        # Iterates over the sub entity items calling
        # the 'DFS' and getting their values and weights
        weights_list, values_list = [], []
        for sub_entity_item in item[sub_entity_name]:
            calculate_entity_item(sub_entity_item)
            weights_list.append(sub_entity_item["weight"])
            values_list.append(sub_entity_item["value"])

        item["value"] = calculate_aggregated_value(values_list, weights_list)

    calculate_entity_item(pre_config["sqc"])

    aggregated_sqc = pre_config["sqc"]["value"]
    return aggregated_sqc


def calculate_measures(dataframe: pd.DataFrame, measures: List[str]) -> Dict[str, float]:
    combined_measures = {}
    for measure in measures:
        combined_measures[measure] = MEASURES_INTERPRETATION_MAPPING[measure]["interpretation_function"](dataframe)

    return combined_measures


def calculate_measure(measure_key: str, metrics: List):
    data = {metric["key"]: metric["value"] for metric in metrics if metric["measure_key"] == measure_key}
    measure_value = MEASURES_INTERPRETATION_MAPPING[measure_key]["calculation_function"](data)
    return measure_value


def calculate_aggregated_value(
    values_list: List[float],
    weights_list: List[float],
) -> float:
    weighted_items = weighting_operation(values_list, weights_list)
    return aggregation_operation(weighted_items, weights_list)


def update_pre_config_dict(pre_config: Dict) -> Dict:
    """
    Creates a new level for the SQC information and adds
    the name of the current entity and the sub entity in each of
    the pre-config items to facilitate the iteration in the DFS algorithm.
    """
    for characteristic in pre_config["characteristics"]:
        characteristic.update({
            "entity": "characteristics",
            "sub_entity": "subcharacteristics",
        })
        for subcharacteristics in characteristic["subcharacteristics"]:
            subcharacteristics.update({
                "entity": "subcharacteristics",
                "sub_entity": "measures",
            })
            for measure in subcharacteristics["measures"]:
                measure.update({
                    "entity": "measures",
                    "sub_entity": "metrics",
                })

    updated_pre_config = {
        "sqc": {
            "entity": "sqc",
            "sub_entity": "characteristics",
            "characteristics": pre_config["characteristics"],
        }
    }

    return updated_pre_config
