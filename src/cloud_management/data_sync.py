import os
import boto3
from botocore.exceptions import ClientError

class DataSync:
    def __init__(self, local_directory, bucket_name):
        self.s3 = boto3.client('s3')
        self.local_directory = local_directory
        self.bucket_name = bucket_name

    def sync_to_cloud(self):
        for root, dirs, files in os.walk(self.local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, self.local_directory)
                s3_path = relative_path.replace("\\", "/")  # Ensure proper S3 key format
                
                try:
                    self.s3.head_object(Bucket=self.bucket_name, Key=s3_path)
                except ClientError:
                    # File doesn't exist in S3 or other error occurred
                    print(f"Uploading {local_path} to {s3_path}")
                    self.s3.upload_file(local_path, self.bucket_name, s3_path)

    def sync_from_cloud(self):
        paginator = self.s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket_name):
            for obj in page.get('Contents', []):
                s3_path = obj['Key']
                local_path = os.path.join(self.local_directory, s3_path)
                
                if not os.path.exists(local_path) or os.path.getmtime(local_path) < obj['LastModified'].timestamp():
                    print(f"Downloading {s3_path} to {local_path}")
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    self.s3.download_file(self.bucket_name, s3_path, local_path)

# Usage
sync = DataSync('/path/to/local/directory', 'your-s3-bucket-name')
sync.sync_to_cloud()
sync.sync_from_cloud()