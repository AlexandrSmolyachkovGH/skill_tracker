from contextlib import contextmanager
from typing import Generator

import boto3

from project.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_DEFAULT_REGION,
    AWS_ENDPOINT,
    AWS_SECRET_ACCESS_KEY,
)


def get_aws_session() -> boto3.session.Session:
    return boto3.session.Session()


@contextmanager
def get_ses_client() -> Generator[boto3.client, None, None]:
    session = get_aws_session()
    client = session.client(
        "ses",
        endpoint_url=AWS_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )
    try:
        yield client
    finally:
        client.close()
