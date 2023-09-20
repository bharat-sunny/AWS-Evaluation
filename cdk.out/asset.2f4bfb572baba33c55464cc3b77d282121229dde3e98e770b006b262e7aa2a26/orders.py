import boto3
import json

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('OrdersTable')

def add_order(event):
    body = json.loads(event['body'])
    order_id = body.get('order_id')
    
    # Check for any other required fields here
    
    orders_table.put_item(Item=body)
    
    # You can send a notification or perform other actions here
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order added successfully'})
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
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }

