from util.exceptions import InvalidThresholdValue, InvalidCheckThreshold


def check_non_complex_files_density(
    min_complex_files_density: float, 
    max_complex_files_density: float
):
    if min_complex_files_density != 0:
        raise InvalidThresholdValue(("min_complex_files_density is not equal to 0"))

    if min_complex_files_density >= max_complex_files_density:
        raise InvalidThresholdValue(
            (
                "min_complex_files_density is greater or equal to"
                " max_complex_files_density"
            )
        )


threshold_check_mapping = {
    "check_non_complex_files_density": check_non_complex_files_density
}


def check_threshold(min: float, max: float, measure: str):
    threshold_check_mapping.get(f"check_{measure}", InvalidCheckThreshold())(min, max)
