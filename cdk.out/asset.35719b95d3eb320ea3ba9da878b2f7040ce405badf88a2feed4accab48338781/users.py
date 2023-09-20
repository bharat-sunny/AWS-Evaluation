# import boto3
# import json

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('UsersTable')

# # Create an identity
# ses = boto3.client('ses')


# def handler(event, context):
#     if event['httpMethod'] == 'GET':
#         # Fetch all users (simplified without pagination)
#         users = table.scan()["Items"]
#         return {
#             "statusCode": 200,
#             "body": json.dumps(users)
#         }
    
#     if event['httpMethod'] == 'POST':
#         # Mock code to insert user
#         body = json.loads(event['body'])
#         user_id = body.get('user_id')
#         name = body.get('name')
#         email = body.get('email')
#         response = ses.verify_email_identity( EmailAddress = email)
#         print(response)
#         table.put_item(Item={'user_id': user_id, 'name': name,'email':email,'verification': False})


#         return {
#             "statusCode": 201,
#             "body": json.dumps({"message": "User created."})
#         }
    
#     return {
#         "statusCode": 400,
#         "body": json.dumps({"message": "Invalid request."})}



import boto3
import json

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('UsersTable')

def add_user(event):
    user_data = json.loads(event['body'])
    users_table.put_item(Item=user_data)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User added successfully'})
    }

def delete_user(event):
    user_id = event['queryStringParameters']['user_id']
    users_table.delete_item(Key={'user_id': user_id})
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User deleted successfully'})
    }

def fetch_user(event):
    user_id = event['queryStringParameters']['user_id']
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
