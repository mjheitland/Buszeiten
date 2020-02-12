# coding=utf8
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import datetime
import pytz


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

weekdayList = [
    442, 512, 542,
    600, 620, 640, 650,
    700, 710, 720, 730, 740, 750,
    800, 820, 840,
    900, 920, 940,
    1000, 1020, 1040,
    1100, 1120, 1140,
    1200, 1220, 1240, 1250,
    1300, 1310, 1320, 1330, 1340, 1350,
    1400, 1410, 1420, 1430, 1440, 1450,
    1500, 1510, 1520, 1530, 1540, 1550,
    1600, 1610, 1620, 1630, 1640, 1650,
    1700, 1710, 1720, 1730, 1740, 1750,
    1800, 1810, 1820, 1830, 1840, 1850,
    1900, 1920, 1940,
    2000,
    2019, 1049, 2119, 2149, 2219, 2249, 2319, 2349
    ]
saturdayList = [
    514, 544,
    614, 644,
    714, 744,
    814, 844,
    900, 920, 940,
    1000, 1020, 1040,
    1100, 1120, 1140,
    1200, 1220, 1240, 1250,
    1300, 1310, 1320, 1330, 1340, 1350,
    1400, 1410, 1420, 1430, 1440, 1450,
    1500, 1510, 1520, 1530, 1540, 1550,
    1600, 1620, 1640,
    1700, 1720, 1740,
    1800,
    1819,             1840, 
    1849, 1919,       1920,
    1949, 2019, 2049, 2119, 2149, 2219, 2249, 2319
    ]

sundayList = [
    719,   749,  819,  849,  919,  949, 1019, 1049, 1119, 1149,
    1219, 1249, 1319, 1349, 1419, 1449, 1519, 1549, 1619, 1649,
    1719, 1749, 1819, 1849, 1919, 1949, 2019, 2049, 2119, 2149,
    2219, 2249, 2319
    ]

busstop = "Moltkestrasse"

def tospeech(dep_time):
    return "%02i:%02i" % (dep_time // 100, dep_time % 100)

# returns a list of up to n busses
def nextFromList(list, time):
    res = []
    for dep_time in list:
        if dep_time > time:
            res.append(tospeech(dep_time))
    return res

def nextBusses():
    n = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    
    weekday = n.weekday()
    # Monday = 0, Sunday = 6
    
    time = n.hour * 100 + n.minute
    
    if weekday == 6:
        return nextFromList(sundayList, time)
    if weekday == 5:
        return nextFromList(saturdayList, time)
    return nextFromList(weekdayList, time)
    
def nextBusAnnouncement():
    busses = nextBusses()
    if len(busses) == 0:
        return "Heute fahren leider keine Busse mehr von %s ab." % busstop
    if len(busses) == 1:
        return "Heute fährt der letzte Bus um %s von %s ab." % busses[0] % busstop
    if len(busses) <= 4:
        return "Heute fahren Busse um %s und %s von %s ab." % (", ".join(busses[:-1]), busses[-1], busstop)
    return "Heute fahren Busse um %s und %s von %s ab. Insgesamt fahren heute noch %i Busse." % (
        ", ".join(busses[:3]), busses[3], busstop, len(busses))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Willkommen"
    speech_output = nextBusAnnouncement()
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Sitzung beended"
    speech_output = "Gute Fahrt!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    return get_welcome_response()

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
