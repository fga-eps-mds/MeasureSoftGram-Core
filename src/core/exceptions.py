
class MeasureSoftGramCoreException(Exception):
    """Base MeasureSoftGram Core exception"""
    pass


class InvalidMetricValue(MeasureSoftGramCoreException):
    """Raised when a invalid metric value is provided to the interpretation function"""
    pass
