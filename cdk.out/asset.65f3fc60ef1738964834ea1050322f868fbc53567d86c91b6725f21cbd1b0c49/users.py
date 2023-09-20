import boto3
import json

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('UsersTable')

# # Create an identity
ses = boto3.client('ses')

def add_user(event):
    body = json.loads(event['body'])
    email = body.get('email')
    users_table.put_item(Item=body)
    response = ses.verify_email_identity( EmailAddress = email)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User added successfully'})
    }

def delete_user(event):
    body = json.loads(event['body'])
    user_id = body.get('user_id')
    users_table.delete_item(Key={'user_id': user_id})
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User deleted successfully'})
    }

def fetch_user(event):
    body = json.loads(event['body'])
    user_id = body.get('user_id')
    response = users_table.get_item(Key={'user_id': user_id})
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'User not found'})
        }

def handler(event, context):
    http_method = event['httpMethod']

    if http_method == 'POST':
        return add_user(event)
    elif http_method == 'GET':
        return fetch_user(event)
    elif http_method == 'DELETE':
        return delete_user(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }