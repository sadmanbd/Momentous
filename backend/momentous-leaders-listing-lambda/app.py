import os
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder

# INDEX_NAME = "hash_generated_total-index"
# hash_generated_daily-index


def lambda_handler(event, context):

    table = __get_table_client()
    LIMIT = 10
    INDEX_NAME = "hash_generated_total-index"
    order = "TOTAL"
    if event["queryStringParameters"] and event["queryStringParameters"].get("limit"):
        LIMIT = event["queryStringParameters"]["limit"]
    if event["queryStringParameters"] and event["queryStringParameters"].get("order"):
        order = event["queryStringParameters"]["order"]
    if order == "DAILY":
        INDEX_NAME = "hash_generated_daily-index"

    PK = _get_pk()
    print("Key: ", json.dumps({"PK": PK}, indent=4))

    try:
        response = table.query(
            KeyConditionExpression=Key("PK").eq(
                PK
            ),  # & Key('shared_on').eq(shared_on),
            IndexName=INDEX_NAME,
            ScanIndexForward=False,
            Limit=int(LIMIT),
            ReturnConsumedCapacity="TOTAL",
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return _response(500, {"status": "DynamoDB Client Error"})
    else:
        items = response["Items"]
        consumed_cap = response["ConsumedCapacity"]
        print("GetItems succeeded:")
        print(json.dumps(items, indent=4, cls=DecimalEncoder))
        print(json.dumps(consumed_cap, indent=4, cls=DecimalEncoder))
    return _response(200, items)


def _get_pk():
    return "MOMENTOUS#user"


# Http response builder


def _response(status_code, json_body):
    body = json.dumps(json_body, cls=DecimalEncoder)

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": body,
    }


def __get_table_client():
    TABLE_NAME = os.getenv("TABLE_NAME")
    # AWS_REGION_DYNAMODB = os.getenv("AWS_REGION_DYNAMODB")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    return table
