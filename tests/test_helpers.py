import pandas as pd
import json
import os

METRICS_LIST = [
    "files",
    "functions",
    "complexity",
    "comment_lines_density",
    "duplicated_lines_density",
    "coverage",
    "ncloc",
    "tests",
    "test_errors",
    "test_failures",
    "test_execution_time",
    "security_rating",
]


def read_json(json_path):
    with open(json_path) as json_file:
        json_obj = json.load(json_file)

    return json_obj


def create_base_component_df(json_list):
    df = pd.DataFrame()

    for i in json_list:
        base_component = read_json(i)

        base_component_data = base_component["baseComponent"]["measures"]

        base_component_df = pd.DataFrame(base_component_data)

        base_component_df["filename"] = os.path.basename(i)

        df = pd.concat([df, base_component_df], ignore_index=True)

    return df


def metric_per_file(json):
    file_json = []

    for component in json["components"]:
        file_json.append(component)

    return file_json


def check_component_is_valid(component, language_extension):
    return (
        component["qualifier"] == "DIR" or component["language"] == language_extension
    )


def generate_file_dataframe_per_release(metric_list, json, language_extension):
    df_columns = metric_list + ["qualifier"]
    df = pd.DataFrame(columns=df_columns)

    for file in json:
        if check_component_is_valid(file, language_extension):
            df.at[file["path"], "qualifier"] = file["qualifier"]
            for measure in file["measures"]:
                df.at[file["path"], measure["metric"]] = measure["value"]

    df.reset_index(inplace=True)
    df = df.rename({"index": "path"}, axis=1).drop(["files"], axis=1)

    return df


def create_file_df(json_list, language_extension="js"):
    df = pd.DataFrame()

    for json_file in json_list:
        file_component = read_json(json_file)

        file_component_data = metric_per_file(file_component)

        file_component_df = generate_file_dataframe_per_release(
            METRICS_LIST, file_component_data, language_extension=language_extension
        )

        file_component_df["filename"] = os.path.basename(json_file)

        df = pd.concat([df, file_component_df], ignore_index=True)

    return df
