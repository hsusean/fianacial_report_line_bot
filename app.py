import os
from datetime import datetime
from flask_cors import CORS
from flasgger import Swagger
from flask import Flask, abort, request
from route.homework import blueprint as blueprint_homework
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

CORS(app)
#doc
Swagger(app)
# app.config["DEBUG"] = True
app.config['SWAGGER'] = {'uiversion': 3}
app.config["JSON_AS_ASCII"] = False

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Fianace Report Bot"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)

# # init api
# app.register_blueprint(blueprint_homework, url_prefix='/api/homework')

# if __name__ == '__main__':
#     app.run(
#         host='https://7702e40dbf62.ngrok.io/callback',#os.getenv('SERV_IP', '172.17.196.230'),
#         # port=9897,#os.getenv('SERV_PORT', 9897),
#         # threaded=True,
#         # debug = True
#     )
    
