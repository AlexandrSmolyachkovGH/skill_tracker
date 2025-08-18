from confluent_kafka import (
    KafkaError,
    KafkaException,
    admin,
)

from logger.logger_conf import logger
from project.settings import (
    KAFKA_ENTRY_POINT,
    KAFKA_FILE_TOPIC,
    PROJECT_ANALYTICS_TOPIC,
    TASK_ANALYTICS_TOPIC,
)


class TopicCreator:
    def __init__(self) -> None:
        self.admin = admin.AdminClient(
            {
                "bootstrap.servers": KAFKA_ENTRY_POINT,
            }
        )

    def prepare_new_topics(
        self,
        topics: list[str],
        num_partitions: int = 2,
        num_replicas: int = 1,
    ) -> list[admin.NewTopic]:
        """
        Create list of NewTopic objects for Kafka AdminClient
        """
        new_topics = [
            admin.NewTopic(
                topic,
                num_partitions=num_partitions,
                replication_factor=num_replicas,
            )
            for topic in topics
        ]
        return new_topics

    def ensure_topics(
        self,
        topics: list[str],
    ) -> None:
        """
        Check the topic exists, create a new topic if it doesn't exist
        """
        new_topics = self.prepare_new_topics(topics)
        fs = self.admin.create_topics(new_topics)
        for topic_name, f in fs.items():
            try:
                f.result(timeout=10)
                logger.info(f"Topic {topic_name} created")
            except KafkaException as e:
                err: KafkaError = e.args[0]
                if err.code() == KafkaError.TOPIC_ALREADY_EXISTS:
                    logger.info(f"Topic {topic_name} already exists")
                else:
                    logger.error(f"Failed to create topic {topic_name}: {err}")


topic_creator = TopicCreator()
topics_for_check: list[str | None] = [
    PROJECT_ANALYTICS_TOPIC,
    TASK_ANALYTICS_TOPIC,
    KAFKA_FILE_TOPIC,
]
