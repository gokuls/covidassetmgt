"""
WSGI config for covidasset project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

#import os

#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covidasset.settings')

#application = get_wsgi_application()



import os
import sys
import site

from django.core.wsgi import get_wsgi_application


site.addsitedir('/home/boss/Documents/covidasset/lib64/python3.7/site-packages/')

sys.path.append('/home/boss/Documents/covidasset/covidassetmgt/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covidasset.settings')

application = get_wsgi_application()

