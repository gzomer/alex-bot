import config
import json
import boto3
import string
import random
import datetime

KENDRA_COMPANY_INDEX = config.KENDRA_COMPANY_INDEX
EXPERT_TICKETS_MODEL_CONFIG = {
    'name': 'expert-tickets',
    'content_type':'text/csv'
}

INITIAL_TICKET_NUMBER = 48000

def ask_knowledge_base(params):
    client = boto3.client('kendra')
    
    response = client.query(
        IndexId = KENDRA_COMPANY_INDEX,
        QueryText=params["query"]
    )

    highlights = get_hightlight_from_response(response)
    return {
        'Summary' : highlights
    }
    
def get_hightlight_from_response(response):
    try:
        highlights = response['ResultItems'][0]['AdditionalAttributes'][0]['Value']['TextWithHighlightsValue']['Text']
        printable = set(string.printable)
        # Remove non-ascii chars
        return ''.join(filter(lambda x: x in printable, highlights))

    except Exception as e:
        return ''


def find_expert(ticket_number, category, priority):
    request_date = datetime.date.today().strftime("%d/%m/%y %H:%M")

    history_tickets = get_history_tickets()

    row = [ticket_number, request_date, priority, '', category,'Open','Unassigned','']
    row = [str(col) for col in row]

    predict_ticket = ','.join(row)

    input_expert = history_tickets + '\n' + predict_ticket

    # Get runtime
    runtime = boto3.Session().client('sagemaker-runtime')

    experts_model = ModelEndpoint(EXPERT_TICKETS_MODEL_CONFIG, runtime)

    result = experts_model.predict(input_expert)

    # Get expert assigned
    return result.split('\n')[1].split(',')[-1]

def create_ticket(params):
    ticket_number = generate_ticket_number()
    category = 'IT Department'

    assigne = find_expert(ticket_number, category, '3-Low');

    return {
        'TicketNumber' : ticket_number,
        'Assignee' : assigne,
        'Category' : category
    }

def generate_ticket_number():
    global INITIAL_TICKET_NUMBER
    INITIAL_TICKET_NUMBER += 1
    return INITIAL_TICKET_NUMBER

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

def get_history_tickets():
    # On a real application this should come from a database. 
    # This is used for the expert model to automatically suggest experts for a ticket
    return """Request ID,Request Submitted Date and Time,Request Priority,Request Resolved Date and Time,Request Category,Request Status,Assigned/Unassigned,Request Resolved By
45000,09/03/19 00:00,3-Low,06/07/19 00:00,IT Department,Close,Assigned,John
45001,10/03/19 00:00,3-Low,10/07/19 00:00,IT Department,Close,Assigned,Paul
45002,10/02/19 00:00,3-Low,10/07/19 00:00,Sales Department,Close,Assigned,George
45003,22/03/19 00:00,3-Low,17/07/19 00:00,Sales Department,Close,Assigned,George
45004,26/04/19 00:00,3-Low,25/07/19 00:00,HR Department,Close,Assigned,George
45005,27/04/19 00:00,3-Low,10/07/19 00:00,Sales Department,Close,Assigned,John
45006,12/02/19 00:00,3-Low,09/07/19 00:00,Sales Department,Close,Assigned,John
45007,05/04/19 00:00,3-Low,07/07/19 00:00,Sales Department,Close,Assigned,John
45008,11/05/19 00:00,3-Low,03/07/19 00:00,HR Department,Close,Assigned,George
45009,12/02/19 00:00,3-Low,21/07/19 00:00,Sales Department,Close,Assigned,John
45010,29/01/19 00:00,3-Low,23/07/19 00:00,HR Department,Close,Assigned,Paul
45011,09/04/19 00:00,3-Low,30/07/19 00:00,HR Department,Close,Assigned,John
45012,27/01/19 00:00,3-Low,16/07/19 00:00,HR Department,Close,Assigned,John
45013,11/04/19 00:00,3-Low,14/07/19 00:00,IT Department,Close,Assigned,George
45014,13/03/19 00:00,3-Low,13/07/19 00:00,Sales Department,Close,Assigned,George
45015,11/03/19 00:00,3-Low,09/07/19 00:00,HR Department,Close,Assigned,John
45016,06/02/19 00:00,3-Low,23/07/19 00:00,IT Department,Close,Assigned,George
45017,05/04/19 00:00,3-Low,06/07/19 00:00,Sales Department,Close,Assigned,Paul
45018,25/04/19 00:00,3-Low,16/07/19 00:00,Sales Department,Close,Assigned,John
45019,10/03/19 00:00,3-Low,26/07/19 00:00,HR Department,Close,Assigned,George
45020,03/01/19 00:00,3-Low,18/07/19 00:00,IT Department,Close,Assigned,Paul
45021,26/05/19 00:00,3-Low,16/07/19 00:00,HR Department,Close,Assigned,George
45022,24/04/19 00:00,3-Low,10/07/19 00:00,Sales Department,Close,Assigned,George
45023,24/04/19 00:00,3-Low,08/07/19 00:00,Sales Department,Close,Assigned,Paul
45024,04/04/19 00:00,3-Low,27/07/19 00:00,Sales Department,Close,Assigned,George
45025,02/02/19 00:00,3-Low,29/07/19 00:00,IT Department,Close,Assigned,George
45026,03/01/19 00:00,3-Low,15/07/19 00:00,Sales Department,Close,Assigned,John
45027,22/03/19 00:00,3-Low,27/07/19 00:00,IT Department,Close,Assigned,Paul
45028,12/05/19 00:00,3-Low,13/07/19 00:00,HR Department,Close,Assigned,John
45029,06/02/19 00:00,3-Low,07/07/19 00:00,Sales Department,Close,Assigned,Paul
45030,05/03/19 00:00,3-Low,07/07/19 00:00,Sales Department,Close,Assigned,George
45031,04/04/19 00:00,3-Low,16/07/19 00:00,Sales Department,Close,Assigned,Paul
45032,12/02/19 00:00,3-Low,29/07/19 00:00,Sales Department,Close,Assigned,George
45033,07/02/19 00:00,3-Low,28/07/19 00:00,Sales Department,Close,Assigned,George
45034,29/01/19 00:00,3-Low,01/07/19 00:00,IT Department,Close,Assigned,Paul
45035,05/01/19 00:00,3-Low,23/07/19 00:00,HR Department,Close,Assigned,George
45036,08/03/19 00:00,3-Low,29/07/19 00:00,HR Department,Close,Assigned,John
45037,21/04/19 00:00,3-Low,25/07/19 00:00,Sales Department,Close,Assigned,John
45038,21/02/19 00:00,3-Low,31/07/19 00:00,IT Department,Close,Assigned,George
45039,25/04/19 00:00,3-Low,25/07/19 00:00,IT Department,Close,Assigned,Paul
45040,31/03/19 00:00,3-Low,26/07/19 00:00,Sales Department,Close,Assigned,John
45041,15/05/19 00:00,3-Low,25/07/19 00:00,IT Department,Close,Assigned,John
45042,27/03/19 00:00,3-Low,14/07/19 00:00,Sales Department,Close,Assigned,George
45043,19/04/19 00:00,3-Low,31/07/19 00:00,IT Department,Close,Assigned,Paul
45044,17/02/19 00:00,3-Low,08/07/19 00:00,IT Department,Close,Assigned,George
45045,30/03/19 00:00,3-Low,08/07/19 00:00,Sales Department,Close,Assigned,John
45046,13/03/19 00:00,3-Low,05/07/19 00:00,Sales Department,Close,Assigned,George
45047,02/04/19 00:00,3-Low,28/07/19 00:00,HR Department,Close,Assigned,John
45048,06/01/19 00:00,3-Low,29/07/19 00:00,Sales Department,Close,Assigned,John
45049,23/04/19 00:00,3-Low,25/07/19 00:00,IT Department,Close,Assigned,Paul
45050,27/01/19 00:00,3-Low,05/07/19 00:00,IT Department,Close,Assigned,Paul
45051,28/04/19 00:00,3-Low,12/07/19 00:00,IT Department,Close,Assigned,George
45052,24/05/19 00:00,3-Low,16/07/19 00:00,IT Department,Close,Assigned,Paul
45053,17/03/19 00:00,3-Low,08/07/19 00:00,Sales Department,Close,Assigned,John
45054,11/05/19 00:00,3-Low,02/07/19 00:00,Sales Department,Close,Assigned,Paul
45055,23/04/19 00:00,3-Low,05/07/19 00:00,Sales Department,Close,Assigned,Paul
45056,04/04/19 00:00,3-Low,08/07/19 00:00,IT Department,Close,Assigned,John
45057,13/05/19 00:00,3-Low,15/07/19 00:00,IT Department,Close,Assigned,John
45058,30/03/19 00:00,3-Low,04/07/19 00:00,Sales Department,Close,Assigned,Paul
45059,25/02/19 00:00,3-Low,23/07/19 00:00,Sales Department,Close,Assigned,Paul
45060,24/05/19 00:00,3-Low,05/07/19 00:00,Sales Department,Close,Assigned,John
45061,16/01/19 00:00,3-Low,05/07/19 00:00,Sales Department,Close,Assigned,John
45062,26/05/19 00:00,3-Low,29/07/19 00:00,Sales Department,Close,Assigned,Paul
45063,24/04/19 00:00,3-Low,29/07/19 00:00,IT Department,Close,Assigned,George
45064,07/01/19 00:00,3-Low,20/07/19 00:00,Sales Department,Close,Assigned,Paul
45065,01/04/19 00:00,3-Low,01/07/19 00:00,Sales Department,Close,Assigned,Paul
45066,24/01/19 00:00,3-Low,06/07/19 00:00,HR Department,Close,Assigned,John
45067,28/05/19 00:00,3-Low,20/07/19 00:00,IT Department,Close,Assigned,George
45068,11/04/19 00:00,3-Low,10/07/19 00:00,Sales Department,Close,Assigned,Paul
45069,29/05/19 00:00,3-Low,24/07/19 00:00,IT Department,Close,Assigned,George
45070,01/01/19 00:00,3-Low,08/07/19 00:00,HR Department,Close,Assigned,Paul
45071,07/01/19 00:00,3-Low,10/07/19 00:00,IT Department,Close,Assigned,Paul
45072,20/01/19 00:00,3-Low,18/07/19 00:00,Sales Department,Close,Assigned,George
45073,24/01/19 00:00,3-Low,03/07/19 00:00,Sales Department,Close,Assigned,John
45074,02/03/19 00:00,3-Low,14/07/19 00:00,Sales Department,Close,Assigned,John
45075,08/02/19 00:00,3-Low,25/07/19 00:00,HR Department,Close,Assigned,John
45076,27/02/19 00:00,3-Low,25/07/19 00:00,Sales Department,Close,Assigned,Paul
45077,28/02/19 00:00,3-Low,24/07/19 00:00,HR Department,Close,Assigned,Paul
45078,22/05/19 00:00,3-Low,13/07/19 00:00,HR Department,Close,Assigned,Paul
45079,16/02/19 00:00,3-Low,10/07/19 00:00,Sales Department,Close,Assigned,John
45080,18/03/19 00:00,3-Low,17/07/19 00:00,IT Department,Close,Assigned,George
45081,15/05/19 00:00,3-Low,21/07/19 00:00,IT Department,Close,Assigned,John
45082,19/04/19 00:00,3-Low,11/07/19 00:00,HR Department,Close,Assigned,John
45083,05/05/19 00:00,3-Low,12/07/19 00:00,IT Department,Close,Assigned,George
45084,18/05/19 00:00,3-Low,21/07/19 00:00,IT Department,Close,Assigned,John
45085,22/04/19 00:00,3-Low,29/07/19 00:00,Sales Department,Close,Assigned,George
45086,09/05/19 00:00,3-Low,21/07/19 00:00,IT Department,Close,Assigned,George
45087,25/05/19 00:00,3-Low,01/07/19 00:00,Sales Department,Close,Assigned,George
45088,17/02/19 00:00,3-Low,05/07/19 00:00,Sales Department,Close,Assigned,George
45089,05/04/19 00:00,3-Low,11/07/19 00:00,Sales Department,Close,Assigned,Paul
45090,24/04/19 00:00,3-Low,09/07/19 00:00,Sales Department,Close,Assigned,John
45091,26/03/19 00:00,3-Low,25/07/19 00:00,IT Department,Close,Assigned,George
45092,12/05/19 00:00,3-Low,19/07/19 00:00,IT Department,Close,Assigned,John
45093,23/04/19 00:00,3-Low,22/07/19 00:00,Sales Department,Close,Assigned,George
45094,26/01/19 00:00,3-Low,01/07/19 00:00,IT Department,Close,Assigned,George
45095,03/03/19 00:00,3-Low,18/07/19 00:00,HR Department,Close,Assigned,George
45096,27/04/19 00:00,3-Low,24/07/19 00:00,IT Department,Close,Assigned,George
45097,12/05/19 00:00,3-Low,15/07/19 00:00,HR Department,Close,Assigned,George
45098,25/02/19 00:00,3-Low,10/07/19 00:00,IT Department,Close,Assigned,John
45098,25/02/19 00:00,3-Low,,IT Department,Open,Unassigned,"""

def lambda_handler(event, context):
    
    if event['action'] == 'ask_knowledge_base':
        return ask_knowledge_base(event)
    if event['action'] == 'create_ticket':
        return create_ticket(event)
        
    return {
        'error' : True,
        'message' : 'Invalid action'
    }
