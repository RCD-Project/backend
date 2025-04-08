import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ClienteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Grupo
        self.group_name = 'clientes'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        
        # Envía el mensaje al grupo
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message,
            }
        )

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ObraConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'obras'
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):

        data = json.loads(text_data)
        print("Mensaje recibido desde el cliente:", data)
        await self.send(text_data=json.dumps({'message': data.get('message', 'Sin mensaje')}))

    async def send_update(self, event):
        """
        Este método se invoca cuando se recibe un mensaje del grupo "obras"
        (por ejemplo, desde la función notificar_cambio_obras).
        """
        message = event['message']
        # Envía el mensaje al WebSocket del cliente
        await self.send(text_data=json.dumps({
            'message': message
        }))
