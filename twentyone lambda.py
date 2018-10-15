from random import shuffle
# --------------- Helpers that build all of the responses ----------------------
deck = [['ace','ace of spade'],[2,'two of spade'],[3,'three of spade'],
          [4,'four of spade'],[5,'five of spade'],[6,'six of spade'],
          [7,'seven of spade'],[8,'eight of spade'],[9,'nine of spade'],
          [10,'spade'],['jack','jack of spade'],['queen','queen of spade'],
          ['king','king of spade'],['ace','ace of diamond'],[2,'two of diamond'],
          [3,'three of diamond'],[4,'four of diamond'],[5,'five of diamond'],
          [6,'six of diamond'],[7,'seven of diamond'],[8,'eight of diamond'],
          [9,'nine of diamond'],[10,'ten of diamond'],['jack','jack of diamond'],
          ['queen','queen of diamond'],['king','king of diamond'],
          ['ace','ace of heart'],[2,'two of heart'],[3,'three of heart'],
          [4,'four of heart'],[5,'five of heart'],[6,'six of heart'],
          [7,'seven of heart'],[8,'eight of heart'],[9,'nine of heart'],
          [10,'ten of heart'],['jack','jack of heart'],['queen','queen of heart'],
          ['king','king of heart'],['ace','ace of club'],[2,'two of club'],
          [3,'three of club'],[4,'four of club'],[5,'five of club'],
          [6,'six of club'],[7,'seven of club'],[8,'eight of club'],
          [9,'nine of club'],[10,'ten of club'],['jack','jack of club'],
          ['queen','queen of club'],['king','king of club']]

def lambda_handler(event, context):
    '''
    Identify the request type
    '''
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
                           
    if event['request']['type'] == "LaunchRequest" :
        return onLaunch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest" :
        return onIntent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest" :
        return onSessionEnd(event['request'], event['session'])
 
# --------------- Events ------------------
def onSessionEnd(sessionEndedRequest, session):
    '''
    This intent will be called when session ends.
    '''
    print("on_session_ended requestId=" + sessionEndedRequest['requestId']
             + ", sessionId=" + session['sessionId'])
        
 
def on_session_started(session_started_request, session):
    """ This intent will be called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def onLaunch(launchRequest, session):
    '''
     When skill is launched this intent will be called
    '''
    return welcome()
 
#---------------builder functions------------------------
def build_speechlet_response(title, output, card_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content': card_output
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

def fallBackIntent():
    '''
    This inten will be called when user says something other than utterences.
    '''
    sessionAttributes = {}
    cardTitle = "Sorry!"
    speechOutput = "<speak>"\
                    "You have spoken something different from utterances,"\
                       " Please try again! "\
                    "</speak>"
    repromptText = None
    cardOutput = "You have spoken something different from utterances, Please try again!"
    shouldEndSession = False
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, cardOutput, repromptText, shouldEndSession))

#------------------intent function----------------------            
def onIntent(intentRequest, session):
    '''
    Identify which intent is called.
    '''
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']

    if intentName == "twentyone":
        return twentyone(intent, session)
    elif intentName == "stay_intent":
        return stay_intent(intent, session)
    elif intentName == "rules_intent":
        return rules_intent(intent, session)
    elif intentName == "AMAZON.HelpIntent":
        return rules_intent(intent, session)
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest()
    elif intentName == "AMAZON.FallbackIntent":
        return fallBackIntent()
    else:
        raise ValueError("Invalid intent")

# --------------- Functions that control the skill's behavior ------------------

def welcome():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global deck
    shuffle(deck)
    shuffled = deck
    top = 0
    user_score = 0
    session_attributes = {'score': user_score,
                            'shuffled': shuffled,
                            'top': top}
    card_title = "Welcome"
    speech_output = "<speak>"\
                    "Welcome to the game of twenty one."\
                    "<audio src='https://s3.amazonaws.com/ask-soundlibrary/foley/amzn_sfx_glasses_clink_01.mp3'/>"\
                    " There is a deck of"\
                    " shuffled cards.<break/> You need to hit the top card until you "\
                    " score <emphasis level='moderate'>twenty one. </emphasis>" \
                    "If you are new to this game<break/> then you can ask for rules "\
                    "by saying,<emphasis level='moderate'> tell me the rules.</emphasis>"\
                    " Or You can start the game by saying, " \
                    "<emphasis level='moderate'> lets start twenty one.</emphasis> "\
                    "</speak>"\
                    
    reprompt_text = "You can start the game by saying, lets start twenty one. "
    card_output =  "Welcome to the world of twenty one."\
                    " There is a deck of"\
                    " shuffled cards. You need to hit the top card until you "\
                    " score twenty one. " \
                    "If you are new to this game then you can ask for rules "\
                    "by saying, tell me the rules."\
                    " Or You can start the game by saying, " \
                    " lets start twenty one."
                                   
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

def rules_intent(intent,session):
    '''
    This intent will be calledn when user asks for rules. 
    '''
    shuffled = session['attributes']['shuffled']
    top = session['attributes']['top']
    user_score = session['attributes']['score']
    session_attributes = {'score': user_score,
                            'shuffled': shuffled,
                            'top': top}
    should_end_session = False
    speech_output =  "<speak>"\
                     "Rules are."\
                     " There is a deck of shuffled card.<break/><emphasis level='moderate'> Each card has a point value based on its rank, the suit is ignored in this game."\
                     " <break/>"\
                     " The cards with ranks 2 through 10 have point values of 2 through 10 respectively."\
                     " <break/>The cards Jack, Queen, King have a point value of ten each.<break/> The Ace is considered as 11 points,"\
                     " unless that puts the player over a total of 21 points,<break/> in which case it reverts to 1 point instead. "\
                     " You can win this game only in two cases.</emphasis>"\
                     " first,<break/> If you score exactly twenty one."\
                     " Second,<break/> If you score more than me but less than twenty one."\
                     " I will play after you.<break/> It is Totally a luck based game. Good luck."\
                     " You can resume your game by saying,<emphasis level='strong'> start twenty one.</emphasis>" \
                     "</speak>"
    reprompt_text = "You can resume your game by saying, lets start twenty one."
    card_title = 'twenty one'
    card_output = "Rules are."\
                     " There is a deck of shuffled card. Each card has a point value based on its rank, the suit is ignored in this game."\
                     " The cards with ranks 2 through 10 have point values of 2 through 10 respectively."\
                     " The cards Jack, Queen, King have a point value of ten each. The Ace is considered as 11 points,"\
                     " unless that puts the player over a total of 21 points, in which case it reverts to 1 point instead. "\
                     " You can win this game only in two cases."\
                     " first, If you score exactly twenty one."\
                     " Second, If you score more than me but less than twenty one."\
                     " I will play after you. It is Totally a luck based game. Good luck."\
                     " You can resume your game by saying, start twenty one." 
                     
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, None, should_end_session))

def handleSessionEndRequest():
    '''
    It will handle session end request.
    '''
    card_title = "Session Ended"
    
    speech_output = "<speak>"\
                     "<audio src='https://s3.amazonaws.com/ask-soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_02.mp3'/>"\
                    "Thank you for playing game of twenty one. " \
                    "Have a nice day! "\
                    "</speak>"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    card_output = "Thank you for playing game of twenty one. " \
                    "Have a nice day! "
    return build_response({}, build_speechlet_response(
        card_title, speech_output, card_output, None, should_end_session))


#--------------------------------twenty one-----------------------



def calculate_score(topcard,score):
    '''
    Objective: To calculate the score of user and computer
    Input parameters:
                topcard: the topcard which is used to caculate the score
                score: previous score of the user or computer
    Return value: current score of user or computer
    '''
    #Approach: According to rules:
         #rank of topcard card is added in the previous score
    
    if(topcard[0] == 'ace'):
        if (score+11 < 21):
            score = score+11
        else: score = score+1
    elif (topcard[0] == 'jack' or topcard[0] == 'queen' or topcard[0] == 'king'):
        score = score+10
    else:
        score=score+topcard[0]
    return score

def twentyone(intent,session):
    '''
    Let the user play the game of twenty one.
    '''
    shuffled = session['attributes']['shuffled']
    top = session['attributes']['top']
    user_score = session['attributes']['score']
    topcard = []
    topcard = shuffled[top]
    top = top+1
    user_score = calculate_score(topcard,user_score)
    print(user_score)
    
    if user_score > 21:
        return lose_intent(intent,session,user_score,topcard)
    elif (user_score == 21):
        return win_intent(intent,session,user_score,topcard)
    else:
        session_attributes = {'score': user_score,
                            'shuffled': shuffled,
                            'top': top}
        should_end_session = False
        speech_output = "<speak>"\
                        "Top card from deck is picked. "\
                        "Your card is " +"<emphasis level='moderate'>" +str(topcard[1]) +" </emphasis> and Your score is "\
                        + str(user_score) +".<audio src='https://s3.amazonaws.com/ask-soundlibrary/foley/amzn_sfx_glasses_clink_01.mp3'/> Now Would you like to Hit or Stay "\
                        "</speak>"
        reprompt_text = "please say HIT or stay"
        card_title = 'Twenty One'
        card_output = "Top card from deck is picked. "\
                        "Your card is "  +str(topcard[1]) +" and Your score is "\
                        + str(user_score) +". Now Would you like to Hit or Stay "
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, card_output, reprompt_text, should_end_session))
        
def lose_intent(intent,session,score,topcard):
    '''
    Called when user loses the game.
    '''
    should_end_session = True
    speech_output = "<speak>"\
                    "Top card from deck is picked. "\
                    "your card <emphasis level='moderate'> "+ str(topcard[1]) + "</emphasis> and Now Your score is "+ str(score) +\
                    ". <say-as interpret-as='interjection'>You Lose.<audio src='https://s3.amazonaws.com/ask-soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_02.mp3'/> The game is over</say-as>"\
                    "</speak>"
    reprompt_text = None
    card_title = 'Twenty One'
    card_output = "Top card from deck is picked. "\
                    "your card "+ str(topcard[1]) + " and Now Your score is "+ str(score) +\
                    " The game is over. "
                    
    return build_response({}, build_speechlet_response(
            card_title, speech_output, card_output, reprompt_text, should_end_session))

def win_intent(intent,session,score,topcard):
    '''
    Called when user wins the game.
    '''
    should_end_session = True
    speech_output = "<speak>"\
                    "Top card from deck is picked. "\
                    "your card is <emphasis level='moderate'> "+ str(topcard[1]) +\
                     "<say-as interpret-as='interjection'>. Wow</say-as>. Your score is "\
                     + str(score) + "<audio src='https://s3.amazonaws.com/ask-soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_02.mp3'/><say-as interpret-as='interjection'> You Won. Great Job</say-as>"\
                     "</speak>"
    reprompt_text = None
    card_title = 'Twenty One'
    card_output = "Wow! Your score is "\
                     + str(score) + "You Won. Great Job!"
                     
    return build_response({}, build_speechlet_response(
            card_title, speech_output, card_output, reprompt_text, should_end_session))

def stay_intent(intent,session):
    '''
    Called when user wants to pick another card.
    '''
    user_score = session["attributes"]["score"]
    top = session["attributes"]["top"]
    shuffled = session['attributes']['shuffled']
    comp_score=0
    while comp_score < 17:
        comp_card = shuffled[top]
        top = top+1
        comp_score = calculate_score(comp_card,comp_score)

    if(comp_score > user_score and comp_score < 21 or comp_score == 21):
        should_end_session = True
        speech_output = "<speak>"\
                        "Your score was "+ str(user_score) +" And I played based"\
                        " on my intelligence. I score " + str(comp_score)\
                        +". <audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_cheer_med_01.mp3'/><say-as interpret-as='interjection'> I  won. Better luck Next time</say-as>. "\
                        "</speak>"
        reprompt_text = None
        card_title = 'Twenty One'
        card_output = "Your score was "+ str(user_score) +" And I played based"\
                        " on my intelligence. I score " + str(comp_score)\
                        +". I  won. Better luck Next time. "
                        
        return build_response({}, build_speechlet_response(
            card_title, speech_output, card_output, reprompt_text, should_end_session))
    elif (comp_score == user_score):
        should_end_session = True
        speech_output =  "<speak>"\
                         "Your score was "+ str(user_score) +" I played based"\
                         " on my intelligence. And my score is " +\
                        str(comp_score)+ ". <audio src='https://s3.amazonaws.com/ask-soundlibrary/cartoon/amzn_sfx_boing_long_1x_01.mp3'/>"\
                        "<say-as interpret-as='interjection'> Its a tie. You played well.</say-as>"\
                        "</speak>"
        reprompt_text = None
        card_title = 'Twenty One'
        card_output =  "Your score was "+ str(user_score) +" I played based"\
                         " on my intelligence. And my score is " +\
                        str(comp_score)+ " Its a tie. You played well."
                        
        return build_response({}, build_speechlet_response(
            card_title, speech_output, card_output, reprompt_text, should_end_session))
    else:
        should_end_session = True
        speech_output = "<speak>"\
                         "your score was "+ str(user_score) +" I played based"\
                         " on my intelligence. And my score is " +\
                         str(comp_score)+ ".<audio src='https://s3.amazonaws.com/ask-soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_02.mp3'/>"\
                         "<say-as interpret-as='interjection'> You  won. Better luck next time to me</say-as>."\
                         "</speak>"
        reprompt_text = None
        card_title = 'Twenty One'
        card_output = "your score was "+ str(user_score) +" I played based"\
                         " on my intelligence. And my score is " +\
                         str(comp_score)+ " You won. Better luck next time to me."
        return build_response({}, build_speechlet_response(
            card_title, speech_output, card_output, reprompt_text, should_end_session))

  
