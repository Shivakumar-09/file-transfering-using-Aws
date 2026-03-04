import os
from dotenv import load_dotenv

# Load variables from .env if it exists
load_dotenv()

class Config:
    # Flask Secret Key for Sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-very-secret-key-123')
    
    # AWS Configuration
    # In EC2 with an IAM role, these can be None as boto3 will auto-discover
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    
    # S3 and DynamoDB Names
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'secure-file-sharing-bucket-shiva2026')
    DYNAMODB_USER_TABLE = os.environ.get('DYNAMODB_USER_TABLE', 'SecureFileUsers')
    DYNAMODB_FILE_TABLE = os.environ.get('DYNAMODB_FILE_TABLE', 'SecureFileMetadata')
    
    # Security
    # Master key for AES (should be 32 bytes for AES-256)
    # In production, this should be pulled from AWS Secrets Manager
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', 'p-W_68_S6v7L_Z6v7L_Z6v7L_Z6v7L_Z=')
