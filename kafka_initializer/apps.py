import os
from typing import cast

from confluent_kafka import Producer
from django.apps import AppConfig

from custom_exceptions.custom import KafkaProducerError
from logger.logger_conf import logger


class KafkaInitializerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kafka_initializer"
    producer = None

    def ready(self) -> None:
        if os.environ.get("RUN_MAIN") != "true":
            logger.info("Skipping Kafka topic creation on autoreload")
            return

        from utils.topic_creator import (  # pylint: disable=C0415
            topic_creator,
            topics_for_check,
        )
        topic_creator.ensure_topics(
            cast(list[str], topics_for_check)
        )

        self.initialize_producer()

        self.register_shutdown_handler()

    @classmethod
    def initialize_producer(cls) -> None:
        if cls.producer is not None:
            logger.warning("Kafka Producer already initialized")
            return
        try:
            from kafka.analytics_producer.producer import (  # pylint: disable=C0415
                KafkaProducer,
            )

            cls.producer = KafkaProducer()
            logger.info("Kafka Producer successfully initialized")
        except KafkaProducerError as e:
            logger.error(f"Failed to initialize Kafka Producer: {e}")
            raise

    @classmethod
    def get_producer(cls) -> Producer:
        if cls.producer is None:
            raise KafkaProducerError("Kafka producer not initialized")
        return cls.producer

    @classmethod
    def register_shutdown_handler(cls) -> None:
        import atexit  # pylint: disable=C0415

        atexit.register(cls.cleanup_producer)
        logger.debug("Registered Kafka Producer shutdown handler")

    @classmethod
    def cleanup_producer(cls) -> None:
        if cls.producer is not None:
            try:
                cls.producer.flush()
                logger.info("Kafka Producer flushed successfully")
            except KafkaProducerError as e:
                logger.error(f"Failed to flush Kafka Producer: {e}")
            finally:
                cls.producer = None


def get_kafka_prod() -> Producer | None:
    try:
        return KafkaInitializerConfig.get_producer()
    except KafkaProducerError:
        return None
