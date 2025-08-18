class WorkerError(Exception):
    """Base class for catching Worker errors."""


class KafkaProducerError(Exception):
    """Base class for catching Kafka Producer errors."""


class SesException(Exception):
    """Base class for catching SES errors."""
