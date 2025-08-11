# flake8: noqa: E402
# pylint: disable=C0413
import json
import os
from typing import cast

import django
from confluent_kafka import (
    Consumer,
)

from custom_exceptions.custom import WorkerError

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "project.settings",
)
django.setup()

from kafka.file_consumer.consumer import kafka_file_consumer as kafka
from logger.logger_conf import logger
from tasks.repositories.task_attachment_repository import (
    task_attachment_repository as repo,
)

if __name__ == "__main__":
    consumer = cast(Consumer, kafka.consumer)

    try:
        while True:
            msg = consumer.poll(timeout=5)

            if msg is None:
                continue

            if msg.error():
                continue

            if msg.value() is None:
                consumer.commit(
                    message=msg,
                    asynchronous=False,
                )
                continue

            try:
                value = json.loads(msg.value().decode("utf-8"))
                key = value["key"]

                logger.debug(f"Received key - {key}")

                attachment_id = key.split("_", 1)[0]

                record = repo.get_attachment_by_id(
                    attachment_id=attachment_id,
                )

                if record and record.file_url == repo.pending_url:
                    updt_record = repo.update_task_attachment(
                        attachment=record,
                        file_url=key,
                    )

                consumer.commit(
                    message=msg,
                    asynchronous=False,
                )

            except WorkerError as e:
                logger.error(e)
                continue
    finally:
        consumer.close()
