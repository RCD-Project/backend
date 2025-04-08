# obras/notificaciones.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notificar_cambio_obras(accion, obra):
    """
    accion: 'alta', 'aprobado', 'rechazado', 'eliminado', 'terminado'
    obra: objeto Obra (se utiliza, por ejemplo, su atributo 'nombre')
    """
    channel_layer = get_channel_layer()
    # Puedes ajustar el mensaje según la acción que se realice
    if accion == 'alta':
        mensaje = f"La obra '{obra.nombre}' ha sido registrada."
    elif accion == 'aprobado':
        mensaje = f"La obra '{obra.nombre}' ha sido aprobada."
    elif accion == 'rechazado':
        mensaje = f"La obra '{obra.nombre}' ha sido rechazada."
    elif accion == 'eliminado':
        mensaje = f"La obra '{obra.nombre}' ha sido eliminada."
    elif accion == 'terminado':
        mensaje = f"La obra '{obra.nombre}' ha sido marcada como terminada."
    else:
        mensaje = f"La obra '{obra.nombre}' ha sido actualizada."

    async_to_sync(channel_layer.group_send)(
        'obras',  # Grupo que se usará en el consumer de obras
        {
            'type': 'send_update',  # Este método se definirá en tu consumer WebSocket
            'message': mensaje,
        }
    )
