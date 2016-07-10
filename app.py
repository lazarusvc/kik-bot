from flask import Flask, request, Response
#*****************************************
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

app = Flask(__name__)
kik = KikApi("Suggestionbot", "de3b3ecd-f085-44a0-9103-f899467ecdf4")
kik.set_configuration(Configuration(webhook="https://calm-caverns-74991.herokuapp.com/incoming"))

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

            '''
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body) ])
            '''
            if 'hi' in message.body.lower() or 'hello' in message.body.lower():
                text = 'Hi {}!'.format(message.from_user)
            else:
                text = 'I don\'t understand message'
                send_text(message.from_user, message.chat_id, text)

    return Response(status=200)

#**********************************************************#
# // HOME ROUTE //
#**********************************************************#
@app.route("/")
def hello():
    return "################\n#  HELLO WORLD!  #\n################"


if __name__ == "__main__":
    app.run(port=33507, debug=True)