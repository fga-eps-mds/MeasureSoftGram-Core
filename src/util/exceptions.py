class MeasureSoftGramCoreException(Exception):
    """Base MeasureSoftGram Core exception"""

    pass


class InvalidMetricValue(MeasureSoftGramCoreException):
    """Raised when a invalid metric value is provided to the interpretation function"""

    pass


class InvalidInterpretationFunctionArguments(MeasureSoftGramCoreException):
    """Raised when invalid arguments are provided to an interpretation function"""

    pass


class ValuesAndWeightsOfDifferentSizes(MeasureSoftGramCoreException):
    """Raised when the length of the weight and values are not equal"""

    pass


class ImplicitMetricValueError(MeasureSoftGramCoreException):
    """
    Exception levantanda quando uma métrica não é passada e não é possível
    obter seu valor de maneira implícita.
    """

    pass


class InvalidThresholdValue(MeasureSoftGramCoreException):
    """Raised when a invalid threshold value is provided to the interpretation function"""

    pass


class InvalidGainInterpretationValue(MeasureSoftGramCoreException):
    """Raised when a invalid gain interpretation value is provided to the interpretation function"""

    pass


class InvalidCheckThreshold(MeasureSoftGramCoreException):
    """Raised when a invalid check threshold function is called"""

    pass


class MeasureKeyNotSupported(MeasureSoftGramCoreException):
    """Raised when a measure key is not supported"""

    pass


class ReleasePlannedAndDevelopedOfDifferentSizes(MeasureSoftGramCoreException):
    """Raised when the sizes of the planned and developed release vectors are different"""

    pass
