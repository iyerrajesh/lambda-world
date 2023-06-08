import logging
import boto3
from botocore.exceptions import ClientError
import os
import uuid
import json
import hashlib

S3_BUCKET = os.environ['s3_bucket']


def get_id():
    """
    Get a 12 char unique ID
    :return:
    """
    uid = uuid.uuid4()
    m = hashlib.md5(uid.bytes)
    return m.hexdigest()[:12]


def persist(url, data):

    file_name = get_id()
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Body=json.dumps(data), Bucket=S3_BUCKET, Key=file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
