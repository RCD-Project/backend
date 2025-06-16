import sys
import os
from django.core.wsgi import get_wsgi_application

# Asegurate que este path coincida con tu estructura real
sys.path.append(os.path.abspath("backend-main/rcdproyect"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rcdproyect.settings")

app = get_wsgi_application()
