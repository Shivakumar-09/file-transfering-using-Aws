import boto3
from botocore.exceptions import ClientError
from config import Config
from datetime import datetime
import uuid

class DatabaseService:
    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            aws_session_token=Config.AWS_SESSION_TOKEN,
            region_name=Config.AWS_REGION
        )
        self.dynamodb = session.resource('dynamodb')
        self.user_table = self.dynamodb.Table(Config.DYNAMODB_USER_TABLE)
        self.file_table = self.dynamodb.Table(Config.DYNAMODB_FILE_TABLE)

    # --- User Management ---
    def create_user(self, email, password_hash, name):
        try:
            self.user_table.put_item(
                Item={
                    'email': email,
                    'name': name,
                    'password_hash': password_hash,
                    'created_at': datetime.utcnow().isoformat()
                },
                ConditionExpression='attribute_not_exists(email)'
            )
            return True
        except ClientError as e:
            print(f"DynamoDB Create User Error: {e}")
            return False

    def get_user(self, email):
        try:
            response = self.user_table.get_item(Key={'email': email})
            return response.get('Item')
        except ClientError as e:
            print(f"DynamoDB Get User Error: {e}")
            return None

    # --- File Metadata Management ---
    def store_file_metadata(self, owner_email, filename, s3_key):
        try:
            file_id = str(uuid.uuid4())
            self.file_table.put_item(
                Item={
                    'file_id': file_id,
                    'owner': owner_email,
                    'filename': filename,
                    's3_key': s3_key,
                    'upload_time': datetime.utcnow().isoformat()
                }
            )
            return file_id
        except ClientError as e:
            print(f"DynamoDB Store Metadata Error: {e}")
            return None

    def get_user_files(self, owner_email):
        """Retrieve all files for a specific user."""
        try:
            # Note: Scan is used here for simplicity. 
            # In production, use Query with a GSI on 'owner'
            response = self.file_table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('owner').eq(owner_email)
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"DynamoDB Query Files Error: {e}")
            return []

    def get_file_metadata(self, file_id):
        try:
            response = self.file_table.get_item(Key={'file_id': file_id})
            return response.get('Item')
        except ClientError as e:
            print(f"DynamoDB Get File Error: {e}")
            return None

    def delete_file_metadata(self, file_id):
        try:
            self.file_table.delete_item(Key={'file_id': file_id})
            return True
        except ClientError as e:
            print(f"DynamoDB Delete Error: {e}")
            return False
