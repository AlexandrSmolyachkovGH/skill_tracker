from celery import shared_task

from custom_exceptions.custom import SesException
from logger.logger_conf import logger
from utils.connections.ses_client import get_ses_client
from utils.ses_messages import ses_messages as msg


@shared_task(name="notifications.deadline_msg.send_deadline_msg")
def send_deadline_msg(
    task_id: str,
    email: str,
) -> None:
    """
    Send notification of the deadline
    """
    try:
        with get_ses_client() as ses:
            ses.send_email(
                Source="sender@example.com",
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": msg.get_deadline_topic()},
                    "Body": {
                        "Text": {
                            "Data": msg.get_deadline_message(
                                task_id=task_id,
                            )
                        }
                    },
                },
            )
    except SesException as e:
        logger.error(f"Error sending email: {e}")
