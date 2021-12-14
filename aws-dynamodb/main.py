import boto3
import json
import random
import os

ACCESS_KEY_ID = os.environ['ACCESS_KEY']
SECRECT_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
REGION = os.environ['REGION']

TABLE_NAME = "TestDynamodb"

VALUE1 = "value1"
VALUE2 = "value2"
NUMBER = 'N'
STRING = 'S'


def putItem(tableName, input):
    dynamodb_client = boto3.client(service_name='dynamodb',
                                   region_name=REGION,
                                   aws_access_key_id=ACCESS_KEY_ID,
                                   aws_secret_access_key=SECRECT_ACCESS_KEY)
    try:
        itemInput = {"TableName": tableName, "Item": input}
        response = dynamodb_client.put_item(**itemInput)
        print("Successfully put item.")
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])


def main():
    with open('summary-object.json') as f:
        contents = f.read()
        object = json.loads(contents)
        object[VALUE1][NUMBER] = str(random.random())
        object[VALUE2][NUMBER] = str(random.random())
        putItem(TABLE_NAME, object)


if __name__ == "__main__":
    main()
