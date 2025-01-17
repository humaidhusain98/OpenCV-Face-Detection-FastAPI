import boto3
SUPPORTED_FILE_TYPES = {
    'image/png':'png',
    'image/jpg':'jpg',
    'image/jpeg':'jpeg',
}

AWS_BUCKET = 'python-opencv-bucket'

session = boto3.Session(
    aws_access_key_id="AKIA37W4OTURBXKBHHG4",
    aws_secret_access_key="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",
)

s3 = session.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)

async def s3_upload(contents: bytes,key: str):
    print(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)
    return {"url":"https://python-opencv-bucket.s3.ap-south-1.amazonaws.com/"+key}