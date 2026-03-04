import boto3
from config import Config

def setup_tables():
    ddb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    
    existing_tables = [t.name for t in ddb.tables.all()]
    print(f"Existing tables: {existing_tables}")

    # 1. Create Users Table
    if Config.DYNAMODB_USER_TABLE not in existing_tables:
        print(f"Creating {Config.DYNAMODB_USER_TABLE}...")
        ddb.create_table(
            TableName=Config.DYNAMODB_USER_TABLE,
            KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
    
    # 2. Create Files Metadata Table
    if Config.DYNAMODB_FILE_TABLE not in existing_tables:
        print(f"Creating {Config.DYNAMODB_FILE_TABLE}...")
        ddb.create_table(
            TableName=Config.DYNAMODB_FILE_TABLE,
            KeySchema=[{'AttributeName': 'file_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'file_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
    
    print("Waiting for tables to become ACTIVE...")
    for table_name in [Config.DYNAMODB_USER_TABLE, Config.DYNAMODB_FILE_TABLE]:
        waiter = ddb.meta.client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
    
    print("Database Setup Complete!")

if __name__ == "__main__":
    setup_tables()
