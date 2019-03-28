from flask import Flask, request, abort
# LINE api
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import requests
import json
import re
from _datetime import datetime
    
app = Flask(__name__)   

#set Line api
KEY = os.environ['DOCOMO_API_KEY']
endpoint = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY=REGISTER_KEY'
url = endpoint.replace('REGISTER_KEY', KEY)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


#　user registration
def register():
    r_endpoint = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/registration?APIKEY=REGISTER_KEY'
    r_url = r_endpoint.replace('REGISTER_KEY', KEY)
    r_headers = {'Content-type': 'application/json'}
    pay = {
        "botId": "Chatting",
        "appKind": "Smart Phone"
    }
    r = requests.post(r_url, data=json.dumps(pay), headers=r_headers)
    appId = r.json()['appId']
    return appId

def reply(appId, utt_content):
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    payload = {
        "language": "ja-JP",
        "botId": "Chatting",
        "appId": appId,
        "voiceText": utt_content,
        "clientData":{
        "option":{"t":"20"} 
        },
        "appRecvTime": "2019-03-27 14:00:00",  
        "appSendTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    # Transmission
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    # rec_time = data['serverSendTime']
    response = data['systemText']['expression']

    print("response: %s" % response)
    return response

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

@app.route("/")
def hello():
    return "Hello World!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    my_text =str(event.message.text)
    
    appId = register()
    print(appId)
    
    utt_content = my_text
    res = reply(appId, utt_content)
        
    res_text = str(res) 
        
    print(str)
    line_bot_api.reply_message(
            event.reply_token,
            #TextSendMessage(text=event.message.text)
            TextSendMessage(text=res_text)
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)