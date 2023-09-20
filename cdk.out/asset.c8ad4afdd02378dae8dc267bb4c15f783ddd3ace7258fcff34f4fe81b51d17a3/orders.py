import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('OrdersTable')

def handler(event, context):
    if event['httpMethod'] == 'GET':
        # Fetch all users (simplified without pagination)
        orders = table.scan()["Items"]
        return {
            "statusCode": 200,
            "body": json.dumps(orders)
        }
    
    if event['httpMethod'] == 'POST':
        # Mock code to insert user
        body = json.loads(event['body'])
        order_id = body.get('order_id')
        name = body.get('name')
        table.put_item(Item={'order_id': order_id, 'name': name})

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Order created."})
        }
    
    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Invalid request."})}



