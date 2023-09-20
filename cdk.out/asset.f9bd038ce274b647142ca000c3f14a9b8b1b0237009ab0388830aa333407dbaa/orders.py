import boto3
import json
import os
import requests

#Environ var 
# notification_lambda_url = os.environ['NOTIFICATION_ENDPOINT']

client = boto3.client('lambda')


dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('OrdersTable')

def add_order(event):
    body = json.loads(event['body'])
    order_id = body.get('order_id')
    



    # Check for any other required fields here
    orders_table.put_item(Item=body)

# ###########################
    # payload = {
    #     "key": "value"
    # }

    # headers = {
    #     "x-api-key": "YOUR_API_KEY"  # If your API Gateway is protected by an API key
    # }

    # # Make the HTTP request
    # response = requests.post(notification_lambda_url, data=json.dumps(payload), headers=headers)
    # print(response)
#     # You can send a notification or perform other actions here


    # response = client.invoke(
    #     FunctionName='TargetLambdaFunctionName',
    #     InvocationType='RequestResponse', # use 'Event' for async invocation
    #     Payload=json.dumps(payload)
    # )
    
    target_lambda_arn = os.environ['TARGET_LAMBDA_ARN']
    
    payload = {
        "key1": "value1",
        "key2": "value2"
    }
    
    response = lambda_client.invoke(
        FunctionName=target_lambda_arn,
        Payload=json.dumps(payload)
    )
    
    response_payload = json.loads(response['Payload'].read())

    response_payload = json.load(response['Payload'])


    print(response_payload)

    return {
        'statusCode': 200,
        'Value': first_lambda_url,
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

