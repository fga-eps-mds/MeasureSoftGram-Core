import pandas as pd


def check_component_is_valid(component, language_extension):

    return (
        component["qualifier"] == "DIR" or component["language"] == language_extension
    )


def create_dataframe(metrics, components, language_extension):

    df_columns = metrics + ["qualifier"]

    df = pd.DataFrame(columns=df_columns)

    for component in components:
        if check_component_is_valid(component, language_extension):
            df.at[component["path"], "qualifier"] = component["qualifier"]
            for metric in component["measures"]:
                df.at[component["path"], metric["metric"]] = metric["value"]

    df.reset_index(inplace=True)
    return df.rename({"index": "path"}, axis=1)
