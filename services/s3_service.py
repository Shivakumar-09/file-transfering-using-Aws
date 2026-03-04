import boto3
from botocore.exceptions import ClientError
from config import Config

class S3Service:
    def __init__(self):
        # boto3 uses IAM roles automatically if running on EC2
        # Use credentials from config if provided (useful for local dev)
        session = boto3.Session(
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            aws_session_token=Config.AWS_SESSION_TOKEN,
            region_name=Config.AWS_REGION
        )
        self.s3_client = session.client('s3')
        self.bucket_name = Config.S3_BUCKET_NAME

    def upload_file(self, file_obj, object_name):
        """Uploads a file-like object to S3."""
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name)
            return True
        except ClientError as e:
            print(f"S3 Upload Error: {e}")
            return False

    def download_file(self, object_name):
        """Downloads a file from S3 and returns bytes."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_name)
            return response['Body'].read()
        except ClientError as e:
            print(f"S3 Download Error: {e}")
            return None

    def delete_file(self, object_name):
        """Deletes an object from S3."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except ClientError as e:
            print(f"S3 Delete Error: {e}")
            return False

    def generate_presigned_url(self, object_name, expiration=300):
        """Generates a temporary download link (default 5 mins)."""
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"S3 Presigned URL Error: {e}")
            return None
