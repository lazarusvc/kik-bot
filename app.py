from flask import Flask, request, Response
import os
#****************************************#
from kik import KikApi, Configuration
from kik.messages import (LinkMessage, SuggestedResponseKeyboard, TextMessage,
                          TextResponse, messages_from_json)


#**********************************************************#
# // Kik Bot Authentication globals
#**********************************************************#
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'Suggestionbot')
BOT_API_KEY = os.environ.get('BOT_API_KEY', 'de3b3ecd-f085-44a0-9103-f899467ecdf4')
BOT_WEBHOOK = os.environ.get('BOT_WEBHOOK', 'https://calm-caverns-74991.herokuapp.com/incoming')


app = Flask(__name__)
kik = KikApi(BOT_USERNAME, BOT_API_KEY)
kik.set_configuration(Configuration(webhook=BOT_WEBHOOK))

#**********************************************************#
# // Kik send.message global function w/
# // keyboards argument 
#**********************************************************#
def send_text(user, chat_id, body, keyboards=[]):
    """Send text."""
    message = TextMessage(to=user, chat_id=chat_id, body=body)
    if keyboards:
        message.keyboards.append(
            SuggestedResponseKeyboard(
                to=user,
                hidden=False,
                responses=[TextResponse(keyboard) for keyboard in keyboards],
            )
        )
    kik.send_messages([message])


#**********************************************************#
# // INCOMING ROUTE //
#**********************************************************#
@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])
    for message in messages:
        if isinstance(message, TextMessage):

            welcome = ["Hi", "Yo", "Hello", "Sup", "Aye"]

            if welcome in message.body:
                text = 'Hi {0}! Welcome to Suggestionbot'.format(message.from_user)
                send_text(message.from_user, message.chat_id, text)
            elif 'Get started' in message.body:
                send_text(message.from_user, message.chat_id, 'Alrightee ... ', ["what Business place where you?"])    
            else:
                text = 'I don\'t understand your message, please Tap "Get started"'
                send_text(message.from_user, message.chat_id, text, ["Get started"])
                    

    return Response(status=200)

#**********************************************************#
# // HOME ROUTE //
#**********************************************************#
@app.route("/")
def hello():
    return "################\n#  HELLO WORLD!  #\n################"


if __name__ == "__main__":
    app.run(port=33507, debug=True)