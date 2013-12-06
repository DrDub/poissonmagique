# This file contains python variables that configure Lamson for email processing.
import logging
import os


handlers = ['app.handlers.game', 'app.handlers.dice', 'app.handlers.log']
upload_handlers = ['app.handlers.upload']

server_name_config = 'localhost'

template_config = {'dir': 'app', 'module': 'templates'}

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

owner_email_config = None
contact_email_config = None
is_silent_config = True


try:
    from localsettings import *
except ImportError:
    pass

relay_config = {'host': relay_name_config, 'port': 25}
receiver_config = { 'host': server_name_config, 'port': 1220 }

router_defaults = {'host': '((%s)|(localhost))' % ( server_name_config, ) }

uploader_queue_sleep = 30
UPLOADER_QUEUE_PATH = "run/upload"


# the config/boot.py will turn these values into variables set in settings
