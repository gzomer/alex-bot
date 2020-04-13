import config
import json
import boto3
import warnings
import requests
import hashlib
import io

warnings.filterwarnings("ignore")
WIREFRAME_CONFIG = {
    'name': 'wireframe',
    'content_type':'image/jpeg',
}

# Wireframe Model
def generate_wireframe(image_url):
    # Get runtime
    runtime = boto3.Session().client('sagemaker-runtime')
    
    # Instantiate our model
    wireframe_model = ModelEndpoint(WIREFRAME_CONFIG, runtime)
    
    # Get image data from S3
    image = get_document_bytes_s3(image_url)
    
    # Perform prediction
    result = wireframe_model.predict(image)
    result_json = json.loads(result)
    
    # Get a HTML from the model result (which is a JSON object)
    content_wireframe = parse_wireframe(result_json)
    
    # Save wireframe on S3
    return save_wireframe(content_wireframe)

# Parse response from model
def parse_wireframe(response):
    html = response['generated_webpage_html'].encode('utf-8').decode('unicode_escape')
    css = response['generated_webpage_css'].encode('utf-8').decode('unicode_escape')
    # Append styles
    html = html.replace('</head>', css + '</head>')
    
    return html

# Store wireframe on S3

def save_wireframe(content):
    s3 = boto3.resource('s3')
    hash_object = hashlib.md5(content.encode('utf-8'))
    file_name = hash_object.hexdigest() +'.html'

    file_s3 = s3.Object(config.BOT_FILES_BUCKET_NAME, file_name)
    
    response = file_s3.put(Body=content)
    return get_full_s3_url(file_name)

def get_full_s3_url(file_name):    
    return 'https://{}.s3.amazonaws.com/{}'.format(config.BOT_FILES_BUCKET_NAME, file_name)

# Get image data from s3
def get_document_bytes_s3(document):
    s3_connection = boto3.resource('s3')
                          
    s3_object = s3_connection.Object(config.BOT_FILES_BUCKET_NAME, document)
    s3_response = s3_object.get()
    
    return s3_response['Body'].read()
    
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
        

# Post helper
def _post_trello(url, params):
    response = requests.post(url,
       data={**params, **config.AUTH_TRELLO}
    )
    
    try: 
        return response.json()
    except:
        raise Exception(response.content)
        
# Get helper
def _get_trello(url, params):
    response = requests.get(
       url,
       data={**params, **config.AUTH_TRELLO}
    )

    try: 
        return response.json()
    except:
        raise Exception(response.content)
    
# Create a card
def create_card(id_list, title):
    url = "https://api.trello.com/1/cards"
    params = {
        'idList': id_list,
        'name': title
    }
    
    return _post_trello(url, params)

# Get all lists in a board
def get_board_lists(id_board):
    url = "https://api.trello.com/1/boards/{}/lists".format(id_board)
    return _get_trello(url, {})

# Add attachment
def add_attachment(id_card, file_url):

    url = 'https://api.trello.com/1/cards/{}/attachments'.format(id_card)
    params = {
        'url': file_url
    }
    return _post_trello(url, params)
    
# Get todo list
def get_todo_list(lists):
    filtered = [list_item for list_item in lists if list_item['name'].lower() == 'todo']
                
    if len(filtered) > 0:
        return filtered[0]
    else:
        return None
            
# Add a task on Trello with attachments
def add_task(params):    
    lists = get_board_lists(config.TRELLO_BOARD_ID)
    todo_list = get_todo_list(lists)
    
    if not todo_list:
        raise Exception('No todo list created on your board')
                
    card = create_card(todo_list['id'], params['name'])
    if not card:
        raise Exception('Error creating your card')            
                
    if 'attachments' in params:
        for attachment in params['attachments']:
            add_attachment(card['id'],attachment['url'])
        
    return card['shortUrl']
                
                
def lambda_handler(event, context):    
    params = {
        'name' : event['Title'].capitalize(),
        'attachments': []
    }
    
    image = event['Image']
    
    # If user has uploaded image, let's call our model and generate a wireframe
    if image:
        params['attachments'].append({'url':image})
        url_wireframe = generate_wireframe(image)
        
        params['attachments'].append({'url':url_wireframe})
        
    # Call Trello API and add a task
    url_card = add_task(params)
    
    return {
        'Url': url_card
    }
