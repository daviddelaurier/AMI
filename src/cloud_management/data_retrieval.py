import boto3
from botocore.exceptions import ClientError

class DataRetrieval:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def list_footage(self, prefix='footage/'):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except ClientError as e:
            print(f"Error listing footage: {e}")
            return []

    def get_presigned_url(self, object_key, expiration=3600):
        try:
            url = self.s3.generate_presigned_url('get_object',
                                                 Params={'Bucket': self.bucket_name,
                                                         'Key': object_key},
                                                 ExpiresIn=expiration)
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def download_footage(self, object_key, local_path):
        try:
            self.s3.download_file(self.bucket_name, object_key, local_path)
            print(f"Downloaded {object_key} to {local_path}")
            return True
        except ClientError as e:
            print(f"Error downloading footage: {e}")
            return False