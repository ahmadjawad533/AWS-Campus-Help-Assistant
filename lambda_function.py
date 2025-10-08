import json
import boto3
import uuid
from datetime import datetime

TABLE_NAME = "Complaints"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    '''
    Lambda handler for Lex fulfillment.
    Expects Lex event structure.
    Intents handled:
      - GreetingIntent
      - ComplaintIntent (slots: UserName, Issue)
      - StatusIntent (slot: ComplaintID)
    '''
    try:
        intent_name = event['currentIntent']['name']
    except Exception as e:
        return close("Sorry, I couldn't understand the request.")

    if intent_name == 'GreetingIntent':
        return close("Hi there!  I’m your Campus Help Assistant. How can I assist you today?")

    elif intent_name == 'ComplaintIntent':
        slots = event['currentIntent'].get('slots') or event.get('sessionState', {}).get('intent', {}).get('slots', {})
        user = get_slot_value(slots, 'UserName')
        issue = get_slot_value(slots, 'Issue')

        if not user or not issue:
            return close("Please provide your name and the issue so I can log your complaint.")

        complaint_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        table.put_item(Item={
            'complaintId': complaint_id,
            'userName': user,
            'issue': issue,
            'status': 'Pending',
            'createdAt': timestamp
        })

        message = f"Thank you {user}! Your complaint has been registered. Complaint ID: {complaint_id}"
        return close(message)

    elif intent_name == 'StatusIntent':
        slots = event['currentIntent'].get('slots') or event.get('sessionState', {}).get('intent', {}).get('slots', {})
        complaint_id = get_slot_value(slots, 'ComplaintID')
        if not complaint_id:
            return close("Please provide the complaint ID you want to check.")

        response = table.get_item(Key={'complaintId': complaint_id})
        if 'Item' in response:
            status = response['Item'].get('status', 'Unknown')
            return close(f"Complaint {complaint_id} status: {status}")
        else:
            return close("Sorry, I couldn't find a complaint with that ID.")

    else:
        return close("Sorry, I didn't understand that intent.")

def get_slot_value(slots, slot_name):
   
    if not slots:
        return None
    val = slots.get(slot_name)
    if isinstance(val, dict):
        v = val.get('value', {}).get('interpretedValue')
        if v:
            return v
        return val.get('value')
    return val

def close(message):
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {'contentType': 'PlainText', 'content': message}
        }
    }
