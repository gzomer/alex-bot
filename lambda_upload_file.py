import config
import hashlib
import json
import boto3
import base64

BUCKET_NAME = config.BOT_FILES_BUCKET_NAME

def get_full_s3_url(file_name):    
    return 'https://{}.s3.amazonaws.com/{}'.format(BUCKET_NAME, file_name)
    
def lambda_handler(event, context):
    
    image = base64.b64decode(event['body']).decode('utf-8')
    
    s3 = boto3.resource('s3',region_name='us-east-1')
    hash_object = hashlib.md5(image.encode('utf-8'))
    file_name = hash_object.hexdigest() +'.jpg'

    file_s3 = s3.Object(BUCKET_NAME, file_name)
    
    response = file_s3.put(Body=base64.b64decode(image))
    
    return {
        'statusCode': 200,
        'body': {
            'success':True,
            'url' : get_full_s3_url(file_name)
        }
    }
