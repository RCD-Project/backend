from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notificar_coordinacion(accion, coordinacion):
    """
    Envía una notificación vía WebSocket para las solicitudes de coordinación.
    
    Parámetros:
      - accion: string, por ejemplo, 'creada', 'aceptada', 'rechazada', 'actualizada'
      - coordinacion: instancia de CoordinacionRetiro
    """
    channel_layer = get_channel_layer()
    # Construimos un mensaje usando datos de la coordinación; ajusta según tus necesidades
    obra_nombre = coordinacion.obra.nombre_obra if coordinacion.obra else "la obra"
    mensaje = f"La coordinación de retiro para {obra_nombre} ha sido {accion}."
    async_to_sync(channel_layer.group_send)(
        "solicitudes",  # Grupo común para notificaciones de solicitudes
        {
            "type": "send_update",  # Este método se definirá en tu consumer (por ejemplo, en un consumer de solicitudes)
            "message": mensaje,
        }
    )
