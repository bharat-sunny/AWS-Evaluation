import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UsersTable')

# Create an identity
ses = boto3.client('ses')


def handler(event, context):
    if event['httpMethod'] == 'GET':
        # Fetch all users (simplified without pagination)
        users = table.scan()["Items"]
        return {
            "statusCode": 200,
            "body": json.dumps(users)
        }
    
    if event['httpMethod'] == 'POST':
        # Mock code to insert user
        body = json.loads(event['body'])
        user_id = body.get('user_id')
        name = body.get('name')
        email = body.get('email')
        response = ses.verify_email_identity( EmailAddress = email)
        print(response)
        table.put_item(Item={'user_id': user_id, 'name': name,'email':email,'verification': False})


        return {
            "statusCode": 201,
            "body": json.dumps({"message": "User created."})
        }
    
    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Invalid request."})}