import os
import urllib.request
import json

def heroku_handler(request, context):
    for event in request['events']:
        # line エンドポイント
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + os.environ['LINE_CHANNEL_SECRET']
        }
        #テキストかスタンプか
        messsage_type = event['message']['type']
        text = ""
        stickerId = ""
        packageId = ""

        if messsage_type == "text":
            text = docomo_chatting(event)

        elif messsage_type == "sticker":
            stickerId = event['message']['StickerId']
            packageId = event['message']['packageId']

        #リクエストbody
        body = {
            'replyToken': event['replyToken'],
            'messages': [
                {
                    "type": messsage_type,
                    "text": text,
                    "stickerId": stickerId,
                    "packageId": packageId 
                }
            ]
        }

        #post 
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), 
        method='POSt', headers=headers)
        with urllib.request.urlopen(req) as res:
            response_body = res.read().decode("utf-8")
    return {'statuCode': 200, 'body': '{}' }

def docomo_chatting(event):
     #docomoエンドポイント
     endpoint = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY=REGISTER_KEY'
     url = endpoint.replace('REGISTER_KEY', os.environ['DOCOMO_API_KEY'])

     # リクエストjson
     text = event['message']['text']
     headers = {"Content-Type":"application/json"}
     body = {
         "language": "ja-JP",
         "botID": "Chatting",
         "appId": os.environ['DOCOMO_APP_ID'],
         "voiceText": text,
         "clientData":{
             "option":{
                 "mode":"dialog",
                 "place":"名古屋"
             }
         }、
         "appRecvTime":"2019-03-27 00:00:00",
         "appSendTime":"2019-03-27 00:00:00"
     }

     #post
     r = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
     with urllib.request.urlopen(r) as r:
         response_body_str = r.read().decode("utf-8")
         response_body = json.loads(response_body_str)
    response = response_body['systemText'][expression]

    return response

