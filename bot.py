import os
from flask import Flask, request, abort
# LINE api
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
# docomo api
import doco.client
    
app = Flask(__name__)   

#set Line api
line_bot_api =LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

#run when accessing "webhook"
@app.route("/webhook", methods=['POST'])
def webhook():
    #get x-line-signature header value
    #set LINE Signature
    signature = request.headers[ 'X-Line-Signature' ]
    #get requset body as text
    #set LINE Message
    body = request.get_data(as_text = True)
    #handle request webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#run when adding values to "handler"
@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    #text from user
    text = event.message.text
    #send text (docomo api) to Line api
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)