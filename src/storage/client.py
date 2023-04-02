import boto3
from botocore.client import BaseClient

from .constants import BUCKET_LOCATION


session = boto3.session.Session()


def get_client_session() -> BaseClient:
    return session.client(service_name='s3', endpoint_url=BUCKET_LOCATION)
