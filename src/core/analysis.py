from src.core.weighting import weighting_operation
from src.core.agregation import agregation_operation
from src.core.constants import MEASURES_INTERPRETATION_MAPPING


def resolve_level(level_dict: dict, sublevel: dict, sublevel_key: str) -> dict:
    aggregated_level = {}
    for key, value in level_dict.items():
        level_items = value[sublevel_key]
        level_weights = value["weights"]

        weights_list = []
        values_list = []

        for idx in range(len(level_items)):
            item = level_items[idx]
            item_value = sublevel[item]
            item_weight = level_weights[item]
            weights_list.append(item_weight)
            values_list.append(item_value)

        weighted_items = weighting_operation(values_list, weights_list)
        aggregated_value = agregation_operation(weighted_items, weights_list)

        aggregated_level[key] = aggregated_value

    return aggregated_level


def make_analysis(measures: dict, subcharacteristics: dict, characteristics: dict):

    aggregated_scs = resolve_level(subcharacteristics, measures, "measures")

    aggregated_characteristics = resolve_level(
        characteristics, aggregated_scs, "subcharacteristics"
    )

    c_weights = {}

    for key, value in characteristics.items():
        c_weights[key] = value["weight"]

    return (
        resolve_level(
            {
                "sqc": {
                    "weights": c_weights,
                    "characteristics": list(aggregated_characteristics.keys()),
                },
            },
            aggregated_characteristics,
            "characteristics",
        ),
        aggregated_scs,
        aggregated_characteristics,
    )


def calculate_measures(dataframe, measures):
    combined_measures = {}
    for measure in measures:
        combined_measures[measure] = MEASURES_INTERPRETATION_MAPPING[measure](dataframe)

    return combined_measures
