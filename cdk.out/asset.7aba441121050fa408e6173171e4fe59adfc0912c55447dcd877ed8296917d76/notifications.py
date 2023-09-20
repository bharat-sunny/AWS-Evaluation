import json
import boto3
import os

ses = boto3.client('ses')
SENDER_EMAIL = "bharattankala@gmail.com"  # Replace with your verified SES email

def handler(event, context):
    # Load the body of the incoming event (order details)
    body_data = json.loads(event['body'])
    
    # Extract the email of the user who placed the order
    recipient_email = body_data.get('Email', '')
    orders = body_data.get('Orders', [])
    
    # Construct the email content
    subject = "Order Confirmation"
    
    # Create a formatted string of order details
    order_details = '\n'.join(['- ' + item for item in orders])
    
    body = f"Thank you for placing your order! Here are the details:\n\n{order_details}"
    
    # Send the email
    response = ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [recipient_email]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Order confirmation email sent via SES!')
    }
