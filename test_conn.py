import boto3
from config import Config

def test_connection():
    try:
        session = boto3.Session(
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            aws_session_token=Config.AWS_SESSION_TOKEN,
            region_name=Config.AWS_REGION
        )
        ddb = session.resource('dynamodb')
        user_table = ddb.Table(Config.DYNAMODB_USER_TABLE)
        print(f"Attempting to scan table: {Config.DYNAMODB_USER_TABLE}...")
        response = user_table.scan(Limit=1)
        print("Success! Connected to DynamoDB.")
        return True
    except Exception as e:
        print(f"Connection Failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
