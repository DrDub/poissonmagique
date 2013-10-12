# This file contains python variables that configure Lamson for email processing.
import logging

# You may add additional parameters such as `username' and `password' if your
# relay server requires authentication, `starttls' (boolean) or `ssl' (boolean)
# for secure connections.
relay_config = {'host': 'localhost', 'port': 8825}

receiver_config = {'host': 'localhost', 'port': 8823}

handlers = ['app.handlers.game']

server_name_config = 'localhost'

template_config = {'dir': 'app', 'module': 'templates'}

os.environ['DJANGO_SETTINGS_MODULE’] = 'webapp.settings’

owner_email_config = None
contact_email_config = None
is_silent_config = True


try:
    from localsettings import *
except ImportError:
    pass

router_defaults = {'host': '((%s)|(localhost))' % [ server_name_config ]}


# the config/boot.py will turn these values into variables set in settings
