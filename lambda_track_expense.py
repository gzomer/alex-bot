import boto3
import config
import json

BUCKET_NAME = config.BOT_FILES_BUCKET_NAME

ADDRESS_EXTRACTOR_CONFIG = {
    'name': 'address-extract',
    'content_type':'text/plain',
}

def get_store(text):
    client_comprehend = boto3.client('comprehend')
    pos = client_comprehend.detect_syntax(
        Text=text,
        LanguageCode='en'
    )
    
    # Get prop nouns
    tokens = [token for token in pos['SyntaxTokens'] if token['PartOfSpeech']['Tag'] == 'PROPN']

    count_propnouns = [[token['Text'], text.lower().count(token['Text'].lower())] for token in tokens]

    count_propnouns.sort(key=lambda x:x[1],reverse=True)

    first_result = count_propnouns[0][0]

    largest_propnouns = [[len(propn), propn] for propn in count_propnouns if first_result.lower() in propn[0].lower() and not propn[0].isupper()] 

    largest_propnouns.sort(key=lambda x:len(x[1][0]),reverse=True)

    store = largest_propnouns[0][1][0]

    return store

def get_price(text):
    client_comprehend = boto3.client('comprehend')
    key_phrases = client_comprehend.detect_key_phrases(
        Text=text,
        LanguageCode='en'
    )
    # Get key phrases that are numbers  
    prices = [word['Text'][1:] for word in key_phrases['KeyPhrases'] if '.' in word['Text'] and len(word['Text']) <= 8]
        
    # Sort by largest price
    prices.sort(key=lambda x:float(x[0]), reverse=True)
    
    # Get largest price
    price = prices[0]
    return price

def get_text_from_image(image_data):        
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(Document={'Bytes': image_data},
                                       FeatureTypes=["TABLES", "FORMS"])
    return response

def get_location_from_model(text):
    # Get runtime
    runtime = boto3.Session().client('sagemaker-runtime')

    address_model = ModelEndpoint(ADDRESS_EXTRACTOR_CONFIG, runtime)

    addresses = address_model.predict(text)

    if addresses == 'No Addresses':
        return None

    return addresses.split('\n')[1]

def get_location_comprehend(text):
    client_comprehend = boto3.client('comprehend')
    entities = client_comprehend.detect_entities(Text=text, LanguageCode='en')
    results = [ent for ent in entities['Entities'] if ent['Type'] == 'LOCATION']
    
    if len(results) > 0:
        return results[0]['Text']
    else:
        return '' 

def get_location(text):
    address = get_location_from_model(text)
    if address:
        return address
    else: #Fallback if the above model doesn't work
        return get_location_comprehend(text)
    
def get_document_bytes_s3(bucket, document):
    s3_connection = boto3.resource('s3')
                          
    s3_object = s3_connection.Object(bucket,document)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream) 
    
    return stream.getvalue()

def get_lines_from_blocks(response):
    return '\n'.join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])

def extract_expense_from_image_data(image_data):
    blocks_text = get_text_from_image(image_data)
    text = get_lines_from_blocks(blocks_text)

    location = get_location(text)
    price = get_price(text)
    store = get_store(text)

    return {
      'Price': price,
      'Location': location,
      'Store' : store
    }

# Generic endpoint model
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

def extract_expense(params):
    image_data = get_document_bytes_s3(BUCKET_NAME, params['Image'])        
    return extract_expense_from_image_data(image_data)
    
def lambda_handler(event, context):
    return extract_expense(event)

