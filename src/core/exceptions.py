class MeasureSoftGramCoreException(Exception):
    """Base MeasureSoftGram Core exception"""

    pass


class InvalidMetricValue(MeasureSoftGramCoreException):
    """Raised when a invalid metric value is provided to the interpretation function"""

    pass


class InvalidInterpretationFunctionArguments(MeasureSoftGramCoreException):
    """Raised when invalid arguments are provided to an interpretation function"""

    pass


class InvalidEqualityOfWeightAndValues(MeasureSoftGramCoreException):
    """Raised when the length of the weight and values are not equal"""

    pass


class InvalidWeightingOperation(MeasureSoftGramCoreException):
    """Raised when the weighting operation return a invalid result"""

    pass
