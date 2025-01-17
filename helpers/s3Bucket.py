import boto3
from env import aws_secret_id,aws_secret_key,s3_bucket_url
SUPPORTED_FILE_TYPES = {
    'image/png':'png',
    'image/jpg':'jpg',
    'image/jpeg':'jpeg',
}

AWS_BUCKET = 'python-opencv-bucket'

session = boto3.Session(
    aws_access_key_id=aws_secret_id,
    aws_secret_access_key=aws_secret_key,
)

s3 = session.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)

async def s3_upload(contents: bytes,key: str):
    print(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)
    return {"url":s3_bucket_url+"/"+key}