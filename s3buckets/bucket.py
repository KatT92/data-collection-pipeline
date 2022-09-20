import boto3
# Let's start by telling to boto3 that we want to use an S3 bucket
s3_client = boto3.client('s3')

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=constants.access_key,
#     aws_secret_access_key=constants.secret_access_key
# )

# response = s3_client.upload_file(file_name, bucket, object_name)
try:
    response = s3_client.upload_file('161936_0.jpg', 'bggdata', '161936_0.jpg')

# Now, let's see the content of the bucket:
#

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('bggdata')

    for file in my_bucket.objects.all():
        print(file.key)

    s3 = boto3.client('s3')

# Of course, change the names of the files to match your own.
    s3.download_file('bggdata', '161936_0.jpg', '161936_0.jpg')
except:
    pass
