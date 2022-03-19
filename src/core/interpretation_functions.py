from .exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
import pandas as pd


def check_arguments(data_frame):
    if not isinstance(data_frame, pd.DataFrame):
        raise InvalidInterpretationFunctionArguments('Expected data_frame to be a pandas.DataFrame')


def check_number_of_files(number_of_files):
    if number_of_files <= 0:
        raise InvalidMetricValue('The number of files is lesser or equal than 0')


def non_complex_files_density(data_frame):
    """
    Calculates non-complex files density (m1).

    This function calculates non-complex files density measure (m1)
    used to assess the changeability quality subcharacteristic.
    """

    CYCLOMATIC_COMPLEXITY_THRESHOLD = 10

    check_arguments(data_frame)

    files_complexity = data_frame['complexity'].astype(float)
    files_functions = data_frame['functions'].astype(float)
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue('The cyclomatic complexity of all files is lesser or equal than 0')

    if files_functions.sum() <= 0:
        raise InvalidMetricValue('The number of functions of all files is lesser or equal than 0')

    files_beneath_threshold_df = data_frame[(files_complexity / files_functions) < CYCLOMATIC_COMPLEXITY_THRESHOLD]

    return len(files_beneath_threshold_df) / number_of_files


def commented_files_density(data_frame):
    """
    Calculates commented files density (m2).

    This function calculates commented files density measure (m2)
    used to assess the changeability quality subcharacteristic.
    """

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    check_arguments(data_frame)

    files_comment_lines_density = data_frame['comment_lines_density'].astype(float)
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

    if files_comment_lines_density.sum() < 0:
        raise InvalidMetricValue('The number of files comment lines density is lesser than 0')

    files_between_thresholds_df = data_frame[files_comment_lines_density.between(
        MINIMUM_COMMENT_DENSITY_THRESHOLD, MAXIMUM_COMMENT_DENSITY_THRESHOLD, inclusive='both')]

    return len(files_between_thresholds_df) / number_of_files


def absence_of_duplications(data_frame):
    """
    Calculates duplicated files absence (m3).

    This function calculates the duplicated files absence measure (m3)
    used to assess the changeability quality subcharacteristic.
    """

    DUPLICATED_LINES_THRESHOLD = 5.0

    check_arguments(data_frame)

    files_duplicated_lines_density = data_frame['duplicated_lines_density'].astype(float)
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue('The number of files duplicated lines density is lesser than 0')

    files_below_threshold_df = data_frame[files_duplicated_lines_density < DUPLICATED_LINES_THRESHOLD]

    return len(files_below_threshold_df) / number_of_files
