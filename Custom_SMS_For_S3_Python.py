
import json
import urllib.parse
import boto3
import os

s3 = boto3.client('s3')
msg = ""

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    # Get bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']
    # Get the object key
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # Get event name
    event_name = event['Records'][0]['eventName']
    event_time = event['Records'][0]['eventTime']
    # Get event region
    event_region = event['Records'][0]['awsRegion']
    sns_response = ""
    
    msg = 'Event {0} triggered for object \"{1}\" from bucket \"{2}\" at {3} in region {4}'.format(event_name, object_key, bucket, event_time,event_region)
    
    if event_name.split(':')[0] != 'ObjectRemoved':
        try:
            response = s3.get_object(Bucket=bucket, Key=object_key)
            msg = msg + ', content type = \"{0}\"'.format(response['ContentType'])
        except Exception as e:
            print('Error getting object {0} from bucket {1}. Make sure they exist and your bucket is in the same region as this function.'.format(object_key, bucket))
    # Create SNS Client
    sns_client = boto3.client('sns')
    # Send SMS
    if msg != "":
        sns_response = sns_client.publish(
            TopicArn=os.environ['topic_arn'],
            Message=msg,
            MessageStructure='string')
            
    return sns_response