from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# from FunctionFolder.WrapperFunc import *


async def callFunc():
    print("websocket callFunc",)
    return True

class MyASyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("Websocket Connected ...", event)
        data = await callFunc()
        print("19 data", data)
#         customData = await Custom2("lalchan", "custom_api", {
#   'a': 10,
#   'b': 20
# })
#         print("23 customData", customData)

        await self.send({
            "type": "websocket.accept" 
        })

       
    async def websocket_receive(self, event):
        print("Websocket Received ...", event)
       
    async def websocket_disconnect(self, event):
        print("Websocket Disconnect ...", event)
        raise StopConsumer()


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("Websocket Connected ...", event)
        self.send({
            "type": "websocket.accept" 
        })

       
    def websocket_receive(self, event):
        print("Websocket Received ...", event)
        print("data", event['text'])
       
        # CodeWriting(eval(event['text'])['code'], eval(event['text'])['user'], eval(event['text'])['api_name'], eval(event['text'])['paramList'])
        

  
    def websocket_disconnect(self, event):
        print("Websocket Disconnect ...", event)
       


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))