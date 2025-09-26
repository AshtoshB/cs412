# file: mini_insta/admin.py
# author: Ashtosh Bhandari ashtosh@bu.edu

"""
ASGI config for cs412 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')

application = get_asgi_application()
