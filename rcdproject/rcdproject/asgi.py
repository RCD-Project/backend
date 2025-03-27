"""
ASGI config for rcdproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import clientes.routing
import obras.routing
import solicitudes.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rcdproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            clientes.routing.websocket_urlpatterns,
            obras.routing.websocket_urlpatterns,
            solicitudes.routing.websocket_urlpatterns,
            
        )
    ),
})
