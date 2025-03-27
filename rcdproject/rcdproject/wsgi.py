"""
WSGI config for rcdproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rcdproject.settings')

application = get_wsgi_application()

# Determinar la raíz del proyecto (la carpeta que contiene 'media')
BASE_DIR = Path(__file__).resolve().parent.parent

# Envolver la aplicación con WhiteNoise
application = WhiteNoise(application)

# Agregar la carpeta 'media' para que se sirva en la URL /media/
application.add_files(str(BASE_DIR / 'media'), prefix='media/')
