# This file contains python variables that configure Lamson for email processing.
import logging

# You may add additional parameters such as `username' and `password' if your
# relay server requires authentication, `starttls' (boolean) or `ssl' (boolean)
# for secure connections.
relay_config = {'host': 'localhost', 'port': 8825}

receiver_config = {'host': 'localhost', 'port': 8823}

handlers = ['app.handlers.sample']

router_defaults = {'host': '((poissonmagique.net)|(localhost))'}

template_config = {'dir': 'app', 'module': 'templates'}

os.environ['DJANGO_SETTINGS_MODULE’] = 'webapp.settings’

# the config/boot.py will turn these values into variables set in settings
