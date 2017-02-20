from __future__ import print_function  # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import decimal
import sys

TASK_COUNT = 3


def fail(msg):
    print(msg)
    sys.exit(1)


def getItem(table, key):
    try:
        response = table.get_item(
            Key={
                'id': key,
            }
        )
    except ClientError as e:
        fail(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return item

class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

session = boto3.Session(profile_name='michal.szewczak')
dynamodb = session.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('whos-cleaning')

item = getItem(table, 'data')
new_state = decimal.Decimal(int(item['appState'] + 1) % TASK_COUNT)
response = table.update_item(
    Key={'id': 'data'},
    UpdateExpression="set appState=:s",
    ExpressionAttributeValues={':s': new_state},
    ReturnValues="UPDATED_NEW"
)
print("UpdateItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))
