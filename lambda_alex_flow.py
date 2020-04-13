import json
import config
from boto3 import client as boto3_client

# AWS Account ID
ACCOUNT_ID = config.ACCOUNT_ID

# Intent names
OPEN_TICKET = 'OpenTicket'
TRACK_EXPENSE = 'TrackExpense'
ADD_TASK = 'AddTask'
ASK_QUESTION = 'AskQuestion'
FIND_DOCUMENT = 'FindDocument'
SEND_PASSPORT = 'SendPassport'

# Lambda functions
TRACK_EXPENSE_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:track_expense'.format(ACCOUNT_ID)
OPEN_TICKET_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:open_ticket'.format(ACCOUNT_ID)
ADD_TASK_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:add_task'.format(ACCOUNT_ID)
ASK_QUESTION_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:ask_question'.format(ACCOUNT_ID)
SEND_PASSPORT_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:send_passport'.format(ACCOUNT_ID)
FIND_DOCUMENT_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:find_document'.format(ACCOUNT_ID)

# Bot messages
_MESSAGES = {
    'DEFAULT': 'Hmm, can you repeat that?',
}

_TRACK_EXPENSE_CONFIG = {
    'lambda_name' : TRACK_EXPENSE_LAMBDA_NAME,
    'slots' : {
        'Price': 'Price'
    },
    'messages' : {
        'NOT_POSSIBLE_DETECT_PRICE': 'What\'s the total amount?',
        'FULFILLED' : 'Great, I have sent this expense for approval.',
        'CONFIRM_MESSAGE' : 'Can you confirm this is an expense of {Price} at {Store} in {Location}?'
    }
}

_ADD_TASK_CONFIG = {
    'lambda_name' : ADD_TASK_LAMBDA_NAME,
    'slots' : {
        'Title': 'Title',
        'Extra': 'Extra',
    },
    'messages' : {
        'ASK_SLOT_TITLE' : 'Sure, what\'s the title of the task?',
        'ASK_SLOT_EXTRA' : 'Great, anything else?',
        'FULFILLED_WIREFRAME' : '''Ok, I have attached the wireframe. I have also created a HTML file based on the image,
        to make your life easier. Here is the link of your new card: {Url}'''
    }
}

_OPEN_TICKET_CONFIG = {
    'lambda_name' : OPEN_TICKET_LAMBDA_NAME,
    'slots' : {
        'Description': 'Description',
        'Summary': 'Summary'
    },
    'messages' : {
        'ASK_SLOT_DESCRIPTION' : 'Sure, what do you need?',
        'CONFIRM_MESSAGE' :'I have about this info about your issue : {Summary}. **Does this solve your problem** ?',
        'FULFILLED_TICKET' : 'Ok then, I have opened a ticket in the category **{Category}** and I have assigned it to **{Assignee}**. \nYour ticket number is **#{TicketNumber}** .',
        'FULFILLED_FOUND_ANSWER': 'That\'s great to hear'
    }
}

_SEND_PASSPORT_CONFIG = {
    'lambda_name' : SEND_PASSPORT_LAMBDA_NAME,
    'slots' : {
        'PassportNumber': 'PassportNumber',
        'BirthDate': 'BirthDate',
        'ExpirationDate': 'ExpirationDate'
    },
    'messages' : {
        'CONFIRM_MESSAGE' :'Do you confirm your passport info is: Passport number: **{PassportNumber}**, Birthdate: **{BirthDate}** and Expiration date: **{ExpirationDate}**?',
        'FULFILLED' : 'Great, I have sent your info to HR.',
        'FAILED' : 'Sorry, it was not possible to identify your passport picture.',
    }
}

_FIND_DOCUMENT_CONFIG = {
    'lambda_name' : FIND_DOCUMENT_LAMBDA_NAME,
    'slots' : {
        'Description': 'Description'
    },
    'messages' : {
        'ASK_SLOT_DESCRIPTION' : 'Sure, what is your document about?',
        'CONFIRM_MESSAGE' :'I have found a document named {Title} and here is the link {Link}. Do you want me to summarize it for you?',
        'FULFILLED' : 'Great, here is the summary: \n\n {Summary}',
        'FAILED' : 'Sorry, no documents match your query.',
    }
}

_ASK_QUESTION_CONFIG = {
    'lambda_name' : ASK_QUESTION_LAMBDA_NAME,
    'slots' : {
        'Description': 'Description'
    },
    'messages' : {
        'FULFILLED' : 'Here is your answer: \n\n {Answer}',
        'FAILED' : 'Sorry, no documents match your query.',
    }
}

# Bot slots
class AttrDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

MESSAGES = AttrDict(_MESSAGES)

def try_ex(func):
    try:
        return func()
    except KeyError:
        return None
        
class Intent():
    def __init__(self, request):
        self.request = request
        self.intent_name = self.request['currentIntent']['name']
        self.confirmation_status = try_ex(lambda: self.request['currentIntent']['confirmationStatus'])
        self.slots = try_ex(lambda: self.request['currentIntent']['slots'])
        self.session_attributes = self.request['sessionAttributes']
        
        self.fix_slots_from_recent_intent()
    
    def fix_slots_from_recent_intent(self):
        if 'recentIntentSummaryView' not in self.request:
            return
        
        if not self.request['recentIntentSummaryView']:
            return
        
        for intent in self.request['recentIntentSummaryView']:
            if intent['intentName'] == self.intent_name and intent['dialogActionType'] == 'ElicitSlot':
                self.slots[intent['slotToElicit']] = self.request['inputTranscript']
        
    def elicit_intent(self, message):
        return {
            'sessionAttributes': self.session_attributes,
            'dialogAction': {
                'type': 'ElicitIntent',
                'message': self._build_message(message)
            }
        }
        
    def elicit_slot(self, slot_to_elicit, message):
        return {
            'sessionAttributes': self.session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': self.intent_name,
                'slots': self.slots,
                'slotToElicit': slot_to_elicit,
                'message': self._build_message(message)
            }
        }
    
    def _build_message(self, message):
        if isinstance(message, str):
            return {'contentType': 'PlainText', 'content': message}
        else:
            return message
    
    def _build_message_markdown(self, message):
        if isinstance(message, str):
            return {'contentType': 'CustomPayload', 'content': message}
        else:
            return message
            
        
    def confirm_intent(self, message):
        return {
            'sessionAttributes': self.session_attributes,
            'dialogAction': {
                'type': 'ConfirmIntent',
                'intentName': self.intent_name,
                'slots': self.slots,
                'message': self._build_message(message)
            }
        }
    
    def fulfill(self, message):
       return self.close('Fulfilled', message)
      
    def fail(self, message):
       return self.close('Failed', message)
        
    def close(self, fulfillment_state, message):
        return {
            'sessionAttributes': self.session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': fulfillment_state,
                'message': self._build_message(message)
            }
        }
    
    def delegate(self, session_attributes, slots):
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': slots
            }
        }
    
    def is_confirmed(self):
        return self.confirmation_status == 'Confirmed'
        
    def is_denied(self):
        return self.confirmation_status == 'Denied'
        
    def has_slot(self, slot):
        return slot in self.slots and self.slots[slot]
    
    def get_slot(self, slot):
        return self.slots[slot]
        
    def set_slot(self, slot, value):
        if not self.slots:
            self.slots = {}
            
        self.slots[slot] = value
        
    def set_session_attr(self, key, value):
        if not self.session_attributes:
            self.session_attributes = {}
            
        self.session_attributes[key] = value
    
    def is_a(self, intent_name):
        return self.intent_name == intent_name
        
        
# Call a model lambda function
class ModelLambdaCaller():
    def __init__(self):
        self.lambda_client = boto3_client('lambda')
        
    def call(self, lambda_name, params):
        invoke_response = self.lambda_client.invoke(FunctionName=lambda_name,
                                               InvocationType='RequestResponse',
                                               Payload=json.dumps(params))
        return json.loads(invoke_response['Payload'].read().decode("utf-8"))
    

# Generic intent handlers
class IntentHandler():
    def __init__(self, intent, config):
        self.intent = intent
        self.SLOTS = AttrDict(config['slots'])
        self.MESSAGES = AttrDict(config['messages'])
        self.LAMBDA_NAME = config['lambda_name']
        
    def call_model(self, params):
        return ModelLambdaCaller().call(self.LAMBDA_NAME, params)
        
    def update_slots(self, slots):
        for key in slots:
            self.intent.slots[key] = slots[key]
            
    def format_message_with_slots(self, message):
        return self.format_message(message, self.intent.slots)
        
    def format_message(self, message, params):
        formatted_message = message
        for key in params:
            formatted_message = formatted_message.replace('{' + key + '}', str(params[key]))
        
        return formatted_message
    
# ------------- Track Expense Intent Flow -------------
class TrackExpenseIntentHandler(IntentHandler):
    def __init__(self, intent):
        super().__init__(intent, _TRACK_EXPENSE_CONFIG)
        
    def get_expense_from_image(self):
        image = ''
        params = {
            'image' : image
        }
        return self.call_model(params)
        
    def fill_expense_slots(self):
        result = self.get_expense_from_image()
        self.update_slots(result)
        
    def format_confirm_message(self):
        return self.format_message_with_slots(self.MESSAGES.CONFIRM_MESSAGE);
        
    def next_state(self):
        if not self.intent.is_confirmed():
            if not self.intent.has_slot(self.SLOTS.Price):
                self.fill_expense_slots()
                
            if self.intent.has_slot(self.SLOTS.Price):    
                return self.intent.confirm_intent(self.format_confirm_message())
            else:
                return self.intent.elicit_slot(elicit_slot, MESSAGES.NOT_POSSIBLE_DETECT_PRICE)
        else:
            return self.intent.fulfill(self.MESSAGES.FULFILLED)

# ------------- Send Passport Intent Flow -------------
class SendPassportIntentHandler(IntentHandler):
    def __init__(self, intent):
        super().__init__(intent, _SEND_PASSPORT_CONFIG)
        
    def get_passport_info(self):
        params = {
            'Image' : self.session_attributes['lastUploadedURL']
        }
        return self.call_model(params)
        
    def format_confirm_message(self):
        return self.format_message_with_slots
        
    def next_state(self):
        if not self.intent.has_slot(self.SLOTS.PassportNumber):
            result = self.get_passport_info()
            self.update_slots(result)
            
        if self.intent.has_slot(self.SLOTS.PassportNumber):
            message = self.format_message_with_slots(self.MESSAGES.CONFIRM_MESSAGE)
            message = self.intent._build_message_markdown(message)
            return self.intent.confirm_intent(message)
        else:
            return self.intent.fail(self.MESSAGES.Failed)
        
        return self.intent.fulfill(self.MESSAGES.FULFILLED)
        
# ------------- Add Task Intent Flow -------------
class AddTaskIntentHandler(IntentHandler):
    def __init__(self, intent):
        super().__init__(intent, _ADD_TASK_CONFIG)
        
    def add_task(self):
        params = {
            'Title' : self.intent.get_slot(self.SLOTS.Title),
            'Image' : self.session_attributes['lastUploadedURL']
        }
        return self.call_model(params)
        
    def next_state(self):
        if not self.intent.has_slot(self.SLOTS.Title):
            return self.intent.elicit_slot(self.SLOTS.Title, self.MESSAGES.ASK_SLOT_TITLE)
            
        if not self.intent.has_slot(self.SLOTS.Extra):
            return self.intent.elicit_slot(self.SLOTS.Extra, self.MESSAGES.ASK_SLOT_EXTRA)
        
        result = self.add_task()
        
        return self.intent.fulfill(self.format_message(self.MESSAGES.FULFILLED_WIREFRAME, result))


# ------------- Find Document Intent Flow -------------
class FindDocumentIntentHandler(IntentHandler):
    def __init__(self, intent):
        super().__init__(intent, _FIND_DOCUMENT_CONFIG)
        
    def find_document(self):
        params = {
            'action': 'find_document',
            'Description' : self.intent.get_slot(self.SLOTS.Description)
        }
        result = self.call_model(params)
        self.update_slots(result)
        
        
    def summarize_document(self):
        params = {
            'action': 'summarize_document',
            'Description' : self.intent.get_slot(self.SLOTS.Description)
        }
        result =  self.call_model(params)
        self.update_slots(result)
        
    def next_state(self):
        if not self.intent.has_slot(self.SLOTS.Description):
            return self.intent.elicit_slot(self.SLOTS.Description, self.MESSAGES.ASK_SLOT_DESCRIPTION)
            
        self.find_document()
        
        if not self.intent.is_confirmed():
            return self.intent.confirm_intent(self.format_message_with_slots(self.MESSAGES.CONFIRM_MESSAGE))
        else:
            self.summarize_document()
            return self.intent.fulfill(self.format_message_with_slots(self.MESSAGES.FULFILLED))
        
# ------------- Ask Question Intent Flow -------------
class AskQuestionIntentHandler(IntentHandler):
    def __init__(self, intent):
        super().__init__(intent, _ASK_QUESTION_CONFIG)
        
    def ask_question(self):
        params = {
            'title' : self.intent.get_slot(self.SLOTS.Description)
        }
        return self.call_model(params)
        
    def next_state(self):
        if not self.intent.has_slot(self.SLOTS.Description):
            return self.intent.elicit_slot(self.SLOTS.Description, self.MESSAGES.ASK_SLOT_DESCRIPTION)
            
        result = self.ask_question()
        
        message = result['Summary']
        
        return self.intent.fulfill(self.format_message(self.MESSAGES.FULFILLED, message))
        
# ------------- Open Ticket Intent Flow -------------
class OpenTicketIntentHandler(IntentHandler):
    def __init__(self, intent):
        super().__init__(intent, _OPEN_TICKET_CONFIG)
    
    def ask_knowledge_base(self):
        params = {
            'query' : self.intent.get_slot(self.SLOTS.Description),
            'action': 'ask_knowledge_base'
        }
        
        result = self.call_model(params)
        self.update_slots(result)
        
        return result
        
    def open_ticket(self):
        params = {
            'description' : self.intent.get_slot(self.SLOTS.Description),
            'action': 'create_ticket'
        }
        return self.call_model(params)
        
    def next_state(self):
        if not self.intent.has_slot(self.SLOTS.Description):
            return self.intent.elicit_slot(self.SLOTS.Description, self.MESSAGES.ASK_SLOT_DESCRIPTION)
        
        if self.intent.is_denied():
            result_ticket = self.open_ticket()
            return self.intent.fulfill(self.intent._build_message_markdown(self.format_message(self.MESSAGES.FULFILLED_TICKET, result_ticket)))
        
        if self.intent.is_confirmed():
            return self.intent.fulfill(self.MESSAGES.FULFILLED_FOUND_ANSWER)
            
        result_knowledge_base = self.ask_knowledge_base()
        
        return self.intent.confirm_intent(self.intent._build_message_markdown(self.format_message(self.MESSAGES.CONFIRM_MESSAGE, result_knowledge_base)))
        

# ------------- Route events to each intent -------------
def dispatch(intent_request):
    intent = Intent(intent_request)
    
    # Remove try/catch
    try:
        if intent.is_a(TRACK_EXPENSE):
            return TrackExpenseIntentHandler(intent).next_state()
            
        if intent.is_a(ADD_TASK):
            return AddTaskIntentHandler(intent).next_state()
        
        if intent.is_a(OPEN_TICKET):
            return OpenTicketIntentHandler(intent).next_state()
            
        if intent.is_a(SEND_PASSPORT):
            return SendPassportIntentHandler(intent).next_state()
            
        if intent.is_a(ASK_QUESTION):
            return AskQuestionIntentHandler(intent).next_state()
            
        if intent.is_a(FIND_DOCUMENT):
            return FindDocumentIntentHandler(intent).next_state()
            
        return intent.elicit_intent(MESSAGES.DEFAULT)
    except Exception as e:        
        return intent.elicit_intent(e)
    
    
    
# ------------- Lambda Starting Point -------------
def lambda_handler(event, context):
    return dispatch(event)
    
    
