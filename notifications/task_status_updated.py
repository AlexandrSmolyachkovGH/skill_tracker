import json

from celery import shared_task

from custom_exceptions.custom import SesException
from logger.logger_conf import logger
from users.repositories.user_project_repository import (
    user_project_repository,
)
from utils.connections.conn_redis import redis_db
from utils.connections.ses_client import get_ses_client
from utils.ses_messages import ses_messages as msg


@shared_task(name="notifications.task_status_updated.send_updated_task")
def send_updated_task() -> None:
    """
    Send task update notification
    """
    logger.info("Task started")
    for key in redis_db.scan_iter(match="update_status:*", count=100):
        record = redis_db.get(key)

        if not record:
            continue
        record_dict = json.loads(record)

        emails = user_project_repository.get_all_user_on_project(
            project_id=record_dict["project_id"],
        )
        logger.info(f"Emails: {emails}")

        try:
            with get_ses_client() as ses:
                ses.send_email(
                    Source="sender@example.com",
                    Destination={"ToAddresses": emails},
                    Message={
                        "Subject": {"Data": msg.get_status_topic()},
                        "Body": {
                            "Text": {
                                "Data": msg.get_status_message(
                                    record_dict["task_id"],
                                    record_dict["project_id"],
                                    record_dict["status"],
                                )
                            }
                        },
                    },
                )

            redis_db.delete(key)

        except SesException as e:
            logger.error(f"Error sending email for key={key}: {e}")
