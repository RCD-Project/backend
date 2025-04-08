import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SolicitudesConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.group_name = 'coordinacion'
    #     await self.channel_layer.group_add(self.group_name, self.channel_name)
    #     await self.accept()
    #     # await self.send(text_data=json.dumps({'message': 'Conectado al WebSocket de solicitudes'}))

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # async def send_update(self, event):
    #     message = event['message']
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
    pass