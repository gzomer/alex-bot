import config
import json
import boto3
import string

KENDRA_COMPANY_INDEX = config.KENDRA_COMPANY_INDEX
NUMBER_OF_SENTENCES = 2

def get_hightlight_from_response(response):
    try:
        highlights = response['ResultItems'][0]['AdditionalAttributes'][0]['Value']['TextWithHighlightsValue']['Text']
        printable = set(string.printable)
        # Remove non-ascii chars
        message = ''.join(filter(lambda x: x in printable, highlights))

        return '.\n'.join(message.split('.')[:NUMBER_OF_SENTENCES])
    except Exception as e:
        return ''
        
def find_document(params):
    client = boto3.client('kendra')
    
    response = client.query(
        IndexId = KENDRA_COMPANY_INDEX,
        QueryText=params["Description"]
    )
    
    highlights = get_hightlight_from_response(response)
    return {
        'Summary' : highlights
    }
    
def lambda_handler(event, context):
    return find_document(event)
