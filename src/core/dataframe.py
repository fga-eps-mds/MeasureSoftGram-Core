# NOTE: Esse dataframe era utilizado nas funções de interpretação, 
#       porém foi retirado devido ao empacotamento.
#       Assim, está comentado caso venha a ser utilizado novamente.

import pandas as pd

from util.check_functions import check_component_is_valid


def create_dataframe(measures, components, language_extension):

    df_columns = measures + ["qualifier"]

    df = pd.DataFrame(columns=df_columns)

    for component in components:
        if check_component_is_valid(component, language_extension):
            df.at[component["path"], "qualifier"] = component["qualifier"]
            for metric in component["measures"]:
                df.at[component["path"], metric["metric"]] = metric["value"]

    df.reset_index(inplace=True)
    return df.rename({"index": "path"}, axis=1)
