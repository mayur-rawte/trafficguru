import json
from flask import request
from flask_restful import reqparse, Resource
import json
import requests
from pprint import pprint
from app.contant import trafficData

class TraffiGuruAPI(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument('hub.verify_token', type=str, location='args')
        self.req_parse.add_argument('hub.challenge', type=str, location='args')

    def get(self):
        args = self.req_parse.parse_args()
        if args['hub.verify_token'] == '2318934571':
            return_challenge = args['hub.challenge']
            return int(return_challenge)
    def post(self):
        incoming_message = request.get_json()
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                fbid = message['sender']['id']
                if 'message' in message:
                    obj = open('traffictest.txt', 'w+')
                    obj.write(str(message))
                    if 'text' in message['message']:
                        custresponse = 'Hi! Nice to see you here. I am TrafficGuru. Yeah Thats what my friends call me coz i know everything about traffic, and probably you are here to get some knowledge about traffic signals. No worries i will master you in that. So lets Start.'
                        post_facebook_message(message['sender']['id'], custresponse, 1)
                        custresponsebtn = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                                 "payload": {
                                                                                                     "template_type": "button",
                                                                                                     "text": "So lets get ready !",
                                                                                                     "buttons": [{
                                                                                                                     "type": "postback",
                                                                                                                     "title": "READY",
                                                                                                                     "payload": "Ready"}]}}}}
                        post_facebook_message(fbid, custresponsebtn, 4)
                    else:
                        post_facebook_message(message['sender']['id'], message['message']['attachments'], 2)
                elif 'postback' in message:
                    text = message['postback']['payload']
                    if text == 'GET_STARTED_PAYLOAD':
                        custresponse = 'Hi! Nice to see you here. I am TrafficGuru. Yeah Thats what my friends call me coz i know everything about traffic, and probably you are here to get some knowledge about traffic signals. No worries i will master you in that. So lets Start.'
                        post_facebook_message(message['sender']['id'], custresponse, 1)
                        custresponsebtn = {"recipient":{"id":fbid }, "message":{"attachment":{"type":"template", "payload":{"template_type":"button", "text":"So lets get ready !", "buttons":[{"type":"postback", "title":"READY", "payload":"Ready"} ] } } } }
                        post_facebook_message(fbid, custresponsebtn, 4)
                    elif text == 'Ready':
                        firstData = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                           "payload": {
                                                                                               "template_type": "generic",
                                                                                               "elements": [{"title":
                                                                                                                 trafficData[
                                                                                                                     'trafficData'][
                                                                                                                     0][
                                                                                                                     'signalName'],
                                                                                                             "image_url":
                                                                                                                 trafficData[
                                                                                                                     'trafficData'][
                                                                                                                     0][
                                                                                                                     'SignalUrl']}]}}}}
                        post_facebook_message(fbid, firstData, 4)
                        firstDataText = trafficData['trafficData'][0]['SignlaDescription']
                        post_facebook_message(fbid, firstDataText, 1)
                        custresponsebtn = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                                 "payload": {
                                                                                                     "template_type": "button",
                                                                                                     "text": "That was Great !",
                                                                                                     "buttons": [{
                                                                                                                     "type": "postback",
                                                                                                                     "title": "Next",
                                                                                                                     "payload": "1"}]}}}}
                        post_facebook_message(fbid, custresponsebtn, 4)
                    else:
                        try:
                            nextData = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                               "payload": {
                                                                                                   "template_type": "generic",
                                                                                                   "elements": [{"title":
                                                                                                                     trafficData[
                                                                                                                         'trafficData'][
                                                                                                                         int(text)][
                                                                                                                         'signalName'],
                                                                                                                 "image_url":
                                                                                                                     trafficData[
                                                                                                                         'trafficData'][
                                                                                                                         int(text)][
                                                                                                                         'SignalUrl']}]}}}}
                            post_facebook_message(fbid, nextData, 4)
                            nextDataText = trafficData['trafficData'][int(text)]['SignlaDescription']
                            post_facebook_message(fbid, nextDataText, 1)
                            custresponsebtn = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                                     "payload": {
                                                                                                         "template_type": "button",
                                                                                                         "text": "That was Great !",
                                                                                                         "buttons": [{
                                                                                                             "type": "postback",
                                                                                                             "title": "Next",
                                                                                                             "payload": int(text)+1}]}}}}

                            a = open("debugorder.txt","w+")
                            a.write(json.dumps(custresponsebtn))
                            a.close()
                            post_facebook_message(fbid, custresponsebtn, 4)
                        except:
                            post_facebook_message(fbid, 'That was all i know, I will be back with some more info. Till then Bye !', 1)
                        #else:
                         #   res = "You now have knowledge of some important traffic signals. I will update myself and get back to you. Thanks"
                         #   post_facebook_message(fbid, custresponsebtn, 1)
                        #custresponse = 'Ruko ! mujhe sikhne de fir tumhe sikhaata hu'
                        #post_facebook_message(message['sender']['id'], custresponse, 1)

def post_facebook_message(fbid, recevied_message,mtype):
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAJrxDp25AwBALee6mEVe9k63GqJmZBzPaCKAPRZBJQ4lzrIbtVTWF4usMGvl77GciY2TmsMvUcyYgcM10NkaDdpn55EcYm47hz1ul4nVWsZBLGYw8RofX2WX46ZBxCHgbbfo0VS2asppm4HZBrlDv9gnmFJ7bavpPfIkoqouzdPWhztrOPlM'
    if mtype == 1:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message": {"text":recevied_message}})
    elif mtype == 2:
        response_msg = json.dumps({"message": {"attachment": {"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/p100x100/851587_369239346556147_162929011_n.png?_nc_ad=z-m&oh=ad2a1e37edd885afb4acd987ad8e33c6&oe=59DEDBB0"}}}, "recipient": {"id": "1346441788784848"}})
    elif mtype == 3:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template", "payload":{"template_type":"button", "text":"I am so excited about this. ", "buttons":[{"type":"postback", "title":"So lets start..", "payload":"signal1"}]}}}})
    elif mtype == 4: #send as it is
        response_msg = json.dumps(recevied_message)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
