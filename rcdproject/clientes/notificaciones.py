from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notificar_cambio_clientes(accion, cliente):
    """
    accion: 'alta' o 'eliminacion'
    cliente: objeto Cliente (se utiliza sus datos para formar el mensaje)
    """
    channel_layer = get_channel_layer()
    mensaje = f"Cliente {cliente.nombre} ha sido {'agregado' if accion=='alta' else 'eliminado'}."
    async_to_sync(channel_layer.group_send)(
        'clientes',
        {
            'type': 'send_update',
            'message': mensaje,
        }
    )
