from __future__ import absolute_import, print_function, unicode_literals
import boto3

# FILL THIS PART
REGION = ''
ACCESS_KEY = ''
SECRET_ACCESS_KEY = ''
DELETE_LAMBDA_NAME = []
DELETE_ALL_LAMBDA_VERSION = False


def clean_old_lambda_versions(all_lambda_version_delete):
    client = boto3.client('lambda',
                          region_name=REGION,
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_ACCESS_KEY
                          )
    functions = client.list_functions()['Functions']
    for function in functions:
        # print(function)
        if all_lambda_version_delete:
            delete_old_version(client, function)
        elif function['FunctionName'] in DELETE_LAMBDA_NAME:
            delete_old_version(client, function)


def delete_old_version(client, function):
    versions = client.list_versions_by_function(FunctionName=function['FunctionArn'])['Versions']
    for version in versions:
        if version['Version'] != function['Version']:
            arn = version['FunctionArn']
            print('delete_function(FunctionName={})'.format(arn))
            # client.delete_function(FunctionName=arn)  # uncomment me once you've checked


if __name__ == '__main__':
    clean_old_lambda_versions(DELETE_ALL_LAMBDA_VERSION)
