from flask import Flask, request, Response
import json
import logging
import os
import re
from datetime import datetime
#****************************************#
from kik import KikApi, Configuration
from kik.messages import (LinkMessage, SuggestedResponseKeyboard, TextMessage, TextResponse, messages_from_json)


#**********************************************************#
# // Kik Bot Authentication globals
#**********************************************************#
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'rant.ai')
BOT_API_KEY = os.environ.get('BOT_API_KEY', 'de3b3ecd-f085-44a0-9103-f899467ecdf4')
BOT_WEBHOOK = os.environ.get('BOT_WEBHOOK', 'https://rant-ai-kik-bot.herokuapp.com/incoming')


app = Flask(__name__)
kik = KikApi(BOT_USERNAME, BOT_API_KEY)
kik.set_configuration(Configuration(webhook=BOT_WEBHOOK))


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['app.db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#**********************************************************#
# // DB model to save messages 
#**********************************************************#
class ChatRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text)
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, original):
        self.original = original

    def __str__(self):
        return self.original

#**********************************************************#
# // Kik send.message global function w/
# // keyboards argument 
#**********************************************************#
def send_text(user, chat_id, body, keyboards=[]):
    """Send text."""
    message = TextMessage(to=user, chat_id=chat_id, body=body)
    if keyboards:
        message.keyboards.append(
            SuggestedResponseKeyboard(to=user, hidden=False, responses=[TextResponse(keyboard) for keyboard in keyboards], ))
    kik.send_messages([message])


#**********************************************************#
# // INCOMING ROUTE //
#**********************************************************#
@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])
    chat_record = ChatRecord(json.dumps(request.json['messages']))
    db.session.add(chat_record)
    db.session.commit()

    for message in messages:
        if isinstance(message, TextMessage):
            logging.info(message)


            if "Hi" in message.body or "Hello" in message.body or "Sup" in message.body:
                text = 'Hi {0}! Welcome to Propos.ai ChatBot. The first Text based solution for voicing your concerns on bad service. Type "HELP" at any time for further instructions or just start Ranting with Hashtag_Business (e.g. #eCorps), we will distribute to the right parties accordingly.'.format(message.from_user)
                send_text(message.from_user, message.chat_id, text)
            elif 'Get started' in message.body:
                send_text(message.from_user, message.chat_id, 'Alrightee ... ', ["Where were you?", "I want to voice a concern", "Business place I can propose to"])    
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