import pandas as pd
import json
import os
import numpy as np
import tensorly as ts
from .interpretation_functions import non_complex_files_density, commented_files_density, absence_of_duplications

METRICS_LIST = [
    'files',
    'functions',
    'complexity',
    'comment_lines_density',
    'duplicated_lines_density',
    'coverage',
    'ncloc',
    'tests',
    'test_errors',
    'test_failures',
    'test_execution_time',
    'security_rating'
]


def read_json(json_path):

    with open(json_path) as json_file:
        json_obj = json.load(json_file)

    return json_obj


def create_base_component_df(json_list):

    df = pd.DataFrame()

    for i in json_list:

        base_component = read_json(i)

        base_component_data = base_component['baseComponent']['measures']

        base_component_df = pd.DataFrame(base_component_data)

        base_component_df['filename'] = os.path.basename(i)

        df = pd.concat([df, base_component_df], ignore_index=True)

    return df


def metric_per_file(json):

    file_json = []

    for component in json['components']:
        if component['qualifier'] == 'FIL':
            file_json.append(component)

    return file_json


def generate_file_dataframe_per_release(metric_list, json, language_extension):

    df_columns = metric_list
    df = pd.DataFrame(columns=df_columns)

    for file in json:
        if file['language'] == language_extension:
            for measure in file['measures']:
                df.at[file['path'], measure['metric']] = measure['value']

    df.reset_index(inplace=True)
    df = df.rename({'index': 'path'}, axis=1).drop(['files'], axis=1)

    return df


def create_file_df(json_list):

    df = pd.DataFrame()

    for i in json_list:

        file_component = read_json(i)

        file_component_data = metric_per_file(file_component)

        file_component_df = generate_file_dataframe_per_release(
            METRICS_LIST, file_component_data, language_extension='js')

        file_component_df['filename'] = os.path.basename(i)

        df = pd.concat([df, file_component_df], ignore_index=True)

    return df


file_component_df = create_file_df(json)

# ________________________________________________________________________________________________________________


def create_metrics_df(df):
    m1_list = [non_complex_files_density(df)]
    m2_list = [commented_files_density(df)]
    m3_list = [absence_of_duplications(df)]

    return pd.DataFrame({'m1': m1_list, 'm2': m2_list, 'm3': m3_list})


def create_sc_tensor(measures_list, size_z):

    return ts.tensor(measures_list).reshape((measures_list.shape[0], measures_list.shape[1], size_z))


def implement_metric_to_tensor():

    measures_list = []
    t_sc_tensor_list = []

    metrics_df = create_metrics_df(file_component_df)

    measures_list.append(np.array([metrics_df['m1'].astype(float),
                                   metrics_df['m2'].astype(float),
                                   metrics_df['m3'].astype(float)]))

    return t_sc_tensor_list.append(create_sc_tensor(measures_list[0], 1))


def t_weighted(t_sc_tensor_list):

    t_sc_weighted_list = []

    metrics_1 = metrics_2 = metrics_3 = 0.3374  # 33%
    SC_EM_Weights = np.array([metrics_1, metrics_2, metrics_3])

    for i in range(len(t_sc_tensor_list)):

        t_sc_weighted = np.empty(t_sc_tensor_list[i].shape)

        for j in range(t_sc_tensor_list[i].ndim):

            t_sc_weighted[:, :, 0][j] = np.tensordot(t_sc_tensor_list[i][:, :, 0][j],
                                                     SC_EM_Weights[j], 0)
        t_sc_weighted_list.append(t_sc_weighted)

    t_sc_weighted_list[0]
