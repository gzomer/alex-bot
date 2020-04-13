import boto3
import config
import json

BUCKET_NAME = config.BOT_FILES_BUCKET_NAME

PASSPORT_CONFIG = {
    'name': 'passport',
    'content_type':'image/jpeg',    
}

def get_passport_from_image(image):
    # Get runtime
    runtime = boto3.Session().client('sagemaker-runtime')

    passport_model = ModelEndpoint(PASSPORT_CONFIG, runtime)

    passport = passport_model.predict(image)

    return passport   

def get_document_bytes_s3(bucket, document):
    s3_connection = boto3.resource('s3')
                          
    s3_object = s3_connection.Object(bucket,document)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream) 
    
    return stream.getvalue()


def extract_info_passport_from_image(image_data):
    passport = get_passport_from_image(image_data)

    passport = json.loads(passport)
    
    return {
        'ExpirationDate': passport['data']['date_of_birth'],
        'BirthDate':  passport['data']['expiration_date'],
        'PassportNumber': passport['data']['number']
    }

def extract_info_passport(event):
    image_data = get_document_bytes_s3(BUCKET_NAME, event['Image'])
    return extract_info_passport_from_image(image_data)

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

def lambda_handler(event, contect):
    return extract_info_passport(event)