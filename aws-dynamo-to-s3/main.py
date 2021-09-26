import csv
import boto3
import os

ACCESS_KEY_ID = os.environ['ACCESS_KEY']
SECRECT_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
REGION = os.environ['REGION']
TABLE_NAME = "TestTable"
S3_BUCKET_NAME = "dynamo-to-s3-tutorial-ilayda"
TEMP_FILENAME = '/tmp/temp.csv'
S3_DATA_KEY = "UPLOADED_DATA"
dynamodb = boto3.resource("dynamodb", aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRECT_ACCESS_KEY,
                          region_name=REGION)
s3 = boto3.resource("s3", aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRECT_ACCESS_KEY,
                    region_name=REGION)
table = dynamodb.Table(TABLE_NAME)
response = table.scan()
items = response['Items']
for item in items:
    print(item)
    with open(TEMP_FILENAME, 'w') as output_file:
        writer = csv.writer(output_file)
        header = True
        first_page = True
        # Paginate results
        while True:
            # Scan DynamoDB table
            if first_page:
                response = table.scan()
                first_page = False
            else:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])

            for item in response['Items']:
                # Write header row?
                if header:
                    writer.writerow(item.keys())
                    header = False
                writer.writerow(item.values())

            # Last page?
            if 'LastEvaluatedKey' not in response:
                break

    # Upload temp file to S3
    s3.Bucket(S3_BUCKET_NAME).upload_file(TEMP_FILENAME, S3_DATA_KEY)

#https://stackoverflow.com/questions/61946504/i-would-like-to-export-dynamodb-table-to-s3-bucket-in-csv-format-using-python-b