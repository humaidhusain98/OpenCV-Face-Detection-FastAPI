import os
localUrl = os.getenv('localUrl')
prodUrl = os.getenv('prodUrl')
isDev = os.getenv('isDev')
aws_secret_id = os.getenv('AWS_SECRET_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
s3_bucket_url = os.getenv('S3_BUCKET_URL')


if isDev=="True":
    url = prodUrl
else:
    url = localUrl