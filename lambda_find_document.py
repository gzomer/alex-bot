import config
import json
import boto3
import string
import re

KENDRA_COMPANY_INDEX = config.KENDRA_COMPANY_INDEX

SUMMARIZER_MODEL_CONFIG = {
    'name': 'summarizer',
    'content_type':'text/plain',
}

# Find documents using Kendra
def find_document(params):
    client = boto3.client('kendra')
    
    response = client.query(
        IndexId = KENDRA_COMPANY_INDEX,
        QueryText=params["Description"]
    )
    
    try:
        result = {
            'Title' : response['ResultItems'][0]['DocumentTitle']['Text'],
            'Link' : response['ResultItems'][0]['DocumentURI']
        }
        return result
    except Exception as e:
        return {}
    
# Summarize documents using SageMaker model
def summarize_document(params):
    # Find document
    document = find_document(params)
    url = document['Link']
    
    # Get document content from S3
    content = get_document_s3(url)
    
    # Instantiate our model
    runtime = boto3.Session().client('sagemaker-runtime')
    summarizer_model = ModelEndpoint(SUMMARIZER_MODEL_CONFIG, runtime)
    
    # Call our model prediction
    response_model = summarizer_model.predict(content)
    
    # Remove info from response (Execution time)
    summary = response_model.split('\n')[0]
    
    return {
        'Summary' : summary
    }

# Generic SageMaker wrapper
class ModelEndpoint():
    
    def __init__(self, config, runtime):           
        self.content_type = config['content_type']
        self.endpoint = config['name']
        self.runtime = runtime
        
    def predict(self, params):          
        # Send data via InvokeEndpoint API
        response = self.runtime.invoke_endpoint(EndpointName=self.endpoint, ContentType=self.content_type, Body=params)
        # Unpack response
        result = response['Body'].read().decode()
        return result   
        
def get_document_s3(url):
    matches = re.search('https://s3.us-east-1.amazonaws.com/(.*)/(.*)', url)
    s3_connection = boto3.resource('s3')
                          
    s3_object = s3_connection.Object(matches[1], matches[2])
    s3_response = s3_object.get()
    
    return s3_response['Body'].read().decode("utf-8") 
    
    
def lambda_handler(event, context):
    
    if event['action'] == 'find_document':
        return find_document(event)
    if event['action'] == 'summarize_document':
        return summarize_document(event)
        
    return {
        'error' : True,
        'message' : 'Invalid action'
    }
