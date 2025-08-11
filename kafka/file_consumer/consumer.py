from confluent_kafka import (
    Consumer,
)

from project.settings import (
    KAFKA_ENTRY_POINT,
    KAFKA_FILE_TOPIC,
)


class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
    ) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.consumer: Consumer | None = None

    def make_config(
        self,
        group_id: str,
        offset_reset: str = "earliest",
        enable_auto_commit: bool = False,
    ) -> dict:
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "auto.offset.reset": offset_reset,
            "group.id": group_id,
            "enable.auto.commit": enable_auto_commit,
        }

    def build(
        self,
        group_id: str,
        offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
    ) -> Consumer:
        """
        Create new Kafka Consumer and subscribe to topic
        """
        if self.consumer is None:
            self.consumer = Consumer(
                self.make_config(
                    group_id=group_id,
                    offset_reset=offset_reset,
                    enable_auto_commit=enable_auto_commit,
                ),
            )
        self.consumer.subscribe([self.topic])
        return self.consumer


kafka_file_consumer = KafkaConsumer(
    bootstrap_servers=KAFKA_ENTRY_POINT or "localhost:9092",
    topic=KAFKA_FILE_TOPIC or "topic",
)

kafka_file_consumer.build(
    group_id="file_consumer",
    enable_auto_commit=False,
)
