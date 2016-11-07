# This file contains python variables that configure Salmon for email processing.
import logging
import os


handlers = ['app.handlers.game', 'app.handlers.log'] # , 'app.handlers.dice'

server_name_config = 'localhost'

template_config = {'dir': 'app', 'module': 'templates'}

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

# the config/boot.py will turn these values into variables set in settings
