import boto3
from botocore.exceptions import ClientError


def bucket_exists(bucket_name, s3):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except:
        return False
    return True


def get_file_contents(bucket_name, object_name, s3):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError:
        return None
    return response['Body']


def copy_contents(source_bucket_name, dest_bucket_name):
    s3_client = boto3.client('s3')

    if not bucket_exists(source_bucket_name, s3_client):
        print("No bucket with name: {}".format(source_bucket_name))
        quit()

    # test code to create old bucket and put some test files
    # if not bucket_exists(source_bucket_name, s3_client):
    #     print("Creating bucket: {}!!".format(source_bucket_name))
    #     s3_client.create_bucket(Bucket=source_bucket_name, ACL='private',
    #                                      CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    #     file_name = 'test1.txt'
    #     s3_client.upload_file(file_name, source_bucket_name, file_name)
    #     file_name = 'test2.txt'
    #     s3_client.upload_file(file_name, source_bucket_name, file_name)

    if not bucket_exists(dest_bucket_name, s3_client):
        print("Creating bucket: {}!!".format(dest_bucket_name))
        s3_client.create_bucket(Bucket=dest_bucket_name, ACL='private',
                                CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})

    print("Files in {}".format(source_bucket_name))
    old_bucket_contents = s3_client.list_objects(Bucket=source_bucket_name).get('Contents') or list()
    for file_obj in old_bucket_contents:
        file_key = file_obj['Key']
        print("File Name: {}".format(file_key))
        file_stream = get_file_contents(source_bucket_name, file_key, s3_client)
        print("File Contents: ")
        print(file_stream.read() if file_stream else None)
        print("-" * 30)

        s3_client.copy_object(CopySource={
            'Bucket': source_bucket_name,
            'Key': file_key,
        }, Bucket=dest_bucket_name, Key=file_key)

    print("Data Copied from Bucket: {} to Bucket:{}".format(source_bucket_name, dest_bucket_name))

    my_bucket_contents = s3_client.list_objects(Bucket=dest_bucket_name).get('Contents') or list()
    print("Files in {}".format(dest_bucket_name))

    for file_obj in my_bucket_contents:
        print(file_obj['Key'])


if __name__ == '__main__':
    source_bucket_name = "sandy-test-1234567"  # Update the source bucket name here
    dest_bucket_name = "sandy-test-1234"  # Update the destination bucket name here
    copy_contents(source_bucket_name, dest_bucket_name)
