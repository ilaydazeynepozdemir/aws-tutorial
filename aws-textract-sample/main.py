import boto3
import os

ACCESS_KEY_ID = os.environ['ACCESS_KEY']
SECRECT_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
textract = boto3.client("textract", aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRECT_ACCESS_KEY,
                        region_name="eu-west-2")

DOCUMENT_PATH = "/home/ilayda/Downloads/"
documentName = DOCUMENT_PATH + "test.png"

with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

response = textract.detect_document_text(Document={'Bytes': imageBytes})

for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print(item["Text"])
