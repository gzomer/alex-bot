# -*- coding: utf-8 -*-
import random
import logging
import config

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import json
from boto3 import client as boto3_client

# Config
ACCOUNT_ID = config.ACCOUNT_ID

ASK_QUESTION_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:ask_question'.format(ACCOUNT_ID)
ADD_TASK_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:add_task'.format(ACCOUNT_ID)
OPEN_TICKET_LAMBDA_NAME = 'arn:aws:lambda:us-east-1:{}:function:open_ticket'.format(ACCOUNT_ID)

# ---------- Messages -------
SKILL_NAME = "Alex"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "I'm your personal assistant. You can ask me questions and much more."
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "I cannot help you with that."

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ------- Ask Question Handler -------
class AskQuestionHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("AskQuestion")(handler_input)

    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        
        if 'Description' in slots:
            ask_question = LambdaCaller(ASK_QUESTION_LAMBDA_NAME)
            
            response = ask_question.call({'Description':slots['Description'].value})
            speech = response['Summary']
        else:
            speech = EXCEPTION_MESSAGE
            
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
        
        
# ------- Add Task Handler -------
class AddTaskHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("AddTask")(handler_input)

    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        
        if 'Title' in slots:
            ask_question = LambdaCaller(ADD_TASK_LAMBDA_NAME)
            
            response = ask_question.call({'Title':slots['Title'].value})
            speech = 'I have added a task named ' + slots['Title'].value
        else:
            speech = EXCEPTION_MESSAGE
            
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
        
# ------- Open Ticket Handler -------
class OpenTicketHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("OpenTicket")(handler_input)

    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        
        if 'Description' in slots:
            open_ticket = LambdaCaller(OPEN_TICKET_LAMBDA_NAME)
            
            response = open_ticket.call({
                'action':'create_ticket',
                'Description':slots['Description'].value
            })
            speech = json.dumps(response)
            
            speech = ('Ok, I have opened a ticket about {} in the category {}, and I have ' +
                       'assigned it to {}. Your ticket number is {}').format(slots['Description'].value, response['Category'], response['Assignee'], response['TicketNumber'])
        else:
            speech = EXCEPTION_MESSAGE
            
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
        
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response

# ------- Status Expense Handler -------
class StatusExpenseHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("StatusExpense")(handler_input)

    def handle(self, handler_input):
        # TODO - Connect with database
        speech = 'You have 1 pending expenses with total of £13.54'
    
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
        
# ------- Hello Handler -------
class HelloHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("Hello")(handler_input))

    def handle(self, handler_input):
        speech = 'Hi, you can ask me questions, track the status of your expenses and even add a task' 
    
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
        
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            FALLBACK_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))

class LambdaCaller():
    def __init__(self, lambda_name):
        self.lambda_name = lambda_name
        self.lambda_client = boto3_client('lambda')
        
    def call(self, params):
        invoke_response = self.lambda_client.invoke(FunctionName=self.lambda_name,
                                               InvocationType='RequestResponse',
                                               Payload=json.dumps(params))
        return json.loads(invoke_response['Payload'].read().decode("utf-8"))

# Register intent handlers
sb.add_request_handler(HelloHandler())
sb.add_request_handler(StatusExpenseHandler())
sb.add_request_handler(AskQuestionHandler())
sb.add_request_handler(AddTaskHandler())
sb.add_request_handler(OpenTicketHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
