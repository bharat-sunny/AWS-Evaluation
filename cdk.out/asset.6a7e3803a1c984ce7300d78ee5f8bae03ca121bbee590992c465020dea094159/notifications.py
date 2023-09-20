import json
import boto3
import os

ses = boto3.client('ses')
SENDER_EMAIL = "sender@example.com"  # Replace with your verified SES email
RECIPIENT_EMAIL = "recipient@example.com"  # Recipient's email

def handler(event, context):
    
    # Sample email data
    subject = "Your SES Notification"
    body = "This is the body of the SES email notification."
    
    response = ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [RECIPIENT_EMAIL]
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
        'body': json.dumps('Email sent via SES!')
    }
