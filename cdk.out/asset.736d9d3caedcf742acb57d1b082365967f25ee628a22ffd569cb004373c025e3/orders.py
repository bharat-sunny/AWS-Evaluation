import boto3
import json
import os

client = boto3.client('lambda')
target_lambda_arn = os.environ['TARGET_LAMBDA_ARN']

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('OrdersTable')

def add_order(event):
    body = json.loads(event['body'])
    email = body.get('email')
    orders = body.get('orders')
    
    orders_table.put_item(Item=body)
    
    payload = {
        "Email": email,
        "Orders": orders
    }
    
    response = client.invoke(
        FunctionName=target_lambda_arn,
        Payload=json.dumps(payload)
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order added successfully'})
    }

def update_order(event):
    body = json.loads(event['body'])
    order_id = body.get('order_id')
    
    # Use update_item to update specific attributes of an item
    expression = "SET email = :e, orders = :o"
    values = {
        ':e': body.get('email'),
        ':o': body.get('orders')
    }

    orders_table.update_item(
        Key={'order_id': order_id},
        UpdateExpression=expression,
        ExpressionAttributeValues=values
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order updated successfully'})
    }

def delete_order(event):
    body = json.loads(event['body'])
    order_id = body.get('order_id')
    orders_table.delete_item(Key={'order_id': order_id})
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order deleted successfully'})
    }

def fetch_order(event):
    body = json.loads(event['body'])
    order_id = body.get('order_id')
    response = orders_table.get_item(Key={'order_id': order_id})
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Order not found'})
        }

def handler(event, context):
    http_method = event['httpMethod']

    if http_method == 'POST':
        return add_order(event)
    elif http_method == 'GET':
        return fetch_order(event)
    elif http_method == 'DELETE':
        return delete_order(event)
    elif http_method == 'PUT':
        return update_order(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }
