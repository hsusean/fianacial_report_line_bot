import os
from datetime import datetime

from flask import Flask, abort, request
from controller.finance_report_crawler import get_each_stock_finance_report
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Fianacial Report Bot"
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

    report_type = get_message[0]
    stock_id = get_message[1:]
    res = get_each_stock_finance_report(stock_id, report_type)
    print(11111, res)
    # Send To Line
    # reply = TextSendMessage(text='''{}'''.format(res))
    reply = ImageSendMessage(
        original_content_url='dataframe.png',
        preview_image_url='dataframe.png'
    )
    line_bot_api.reply_message(event.reply_token, reply)
