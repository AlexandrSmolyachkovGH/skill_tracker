import json

from confluent_kafka import (
    KafkaError,
    Message,
    Producer,
)
from django.core.serializers.json import DjangoJSONEncoder

from custom_exceptions.custom import KafkaProducerError
from logger.logger_conf import logger
from project.settings import (
    KAFKA_ENTRY_POINT,
)


class KafkaProducer:
    def __init__(
        self,
    ) -> None:
        """
        Kafka Producer initialization.
        """
        self.conf = {
            "bootstrap.servers": KAFKA_ENTRY_POINT,
            "message.timeout.ms": 5000,
            "retries": 3,
        }
        self.producer: Producer = Producer(**self.conf)

    def delivery_report(
        self,
        err: KafkaError,
        msg: Message,
    ) -> None:
        """
        Callback for checking delivery status of Kafka producer.
        """
        if err is not None:
            logger.info(f"Delivery failed. Error: {err}")
        else:
            logger.info(
                f"Message {msg.value().decode('utf-8')} delivered to {msg.topic()}"
            )

    def send(self, topic: str, value: dict) -> None:
        """
        Send a message to a Kafka topic.
        """
        try:
            self.producer.produce(
                topic=topic,
                value=json.dumps(
                    value, cls=DjangoJSONEncoder, ensure_ascii=False
                ).encode("utf-8"),
                callback=self.delivery_report,
            )
            self.producer.poll(0)
        except KafkaProducerError as e:
            logger.error(f"Kafka produce error: {e}")

    def flush(self) -> None:
        self.producer.flush()


kafka_producer = KafkaProducer()
