"""
WSGI config for exam project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/exam/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam.settings')
application = get_wsgi_application()
