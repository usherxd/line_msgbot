from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('R7YbuH7w6+KyJ8f8+176eUxHpp3bri+0oPeonl3HmIdRC3gtgoD19Fiy330UNQ9sm05yMxWJcKWXsUzG+7xoYuE8zLOMFaUem5dwBpZYk2lDeKfiW5/T2Oo2zIt+1xA0IzskUVq3VklzrM1EIoAb4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7994d812e171eb454fa82f7bdf41e6e1')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()