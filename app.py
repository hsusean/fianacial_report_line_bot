from flask import Flask
import json, sys, os
from flask_cors import CORS
from flasgger import Swagger
import threading
import json
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from flask import Flask, request, make_response
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
# from database.db_connection import db
from route.homework import blueprint as blueprint_homework


app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
CORS(app)
#doc
Swagger(app)
# app.config["DEBUG"] = True
app.config['SWAGGER'] = {'uiversion': 3}
app.config["JSON_AS_ASCII"] = False

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError as e:
            return make_response("Failure: %s." % str(e), 400)
    return make_response('OK', 200)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)


# init api
app.register_blueprint(blueprint_homework, url_prefix='/api/homework')

if __name__ == '__main__':
    app.run(
        host='https://7702e40dbf62.ngrok.io/callback',#os.getenv('SERV_IP', '172.17.196.230'),
        # port=9897,#os.getenv('SERV_PORT', 9897),
        # threaded=True,
        # debug = True
    )
    
