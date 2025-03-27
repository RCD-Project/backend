import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ClienteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Puedes definir un grupo para enviar mensajes a varios clientes
        self.group_name = 'clientes'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Opcional: si deseas procesar mensajes entrantes
        data = json.loads(text_data)
        message = data.get('message', '')
        # Aquí podrías guardar el mensaje, actualizar alguna tabla, etc.
        
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
        # Nombre del grupo al que se unirán todos los clientes conectados
        self.group_name = 'obras'
        
        # Únete al grupo "obras"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # Puedes enviar un mensaje de bienvenida si lo deseas
        # await self.send(text_data=json.dumps({'message': 'Conectado al WebSocket de obras'}))

    async def disconnect(self, close_code):
        # Al desconectarse, elimina la conexión del grupo
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Opcional: Si deseas procesar mensajes enviados por el cliente,
        puedes implementarlo aquí. Por lo general, para notificaciones en tiempo real,
        el servidor solo envía mensajes a los clientes.
        """
        data = json.loads(text_data)
        # Por ejemplo, podrías imprimir lo recibido o enviar una respuesta
        print("Mensaje recibido desde el cliente:", data)
        # Puedes reenviar el mensaje al mismo cliente si lo deseas:
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
