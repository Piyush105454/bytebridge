"""
WSGI config for bytebridge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebridge.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username="piyush").exists():
    User.objects.create_superuser("piyush", "piyushmodi812@gmail.com", "Code@1")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebridge.settings')

application = get_wsgi_application()
