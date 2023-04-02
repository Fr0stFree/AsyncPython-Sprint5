import boto3
from botocore.client import BaseClient


session = boto3.session.Session()


def get_client_session() -> BaseClient:
    return session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')


# if __name__ == '__main__':
#     s3.upload_file('Makefile', 'async-bucket-5', 'some-key')
#
#     for key in s3.list_objects(Bucket='async-bucket-5')['Contents']:
#         print(key['Key'])
#
#     get_object_response = s3.get_object(Bucket='async-bucket-5', Key='some-key')
#     print(get_object_response['Body'].read())