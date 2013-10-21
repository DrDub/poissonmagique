from config import settings
from lamson.routing import Router
from lamson.server import Relay, SMTPReceiver
from lamson import view, queue
import logging
import logging.config
import jinja2
from app.model import state_storage

logging.config.fileConfig("config/logging.conf")

# the relay host to actually send the final message to
settings.relay = Relay(host=settings.relay_config['host'], 
                       port=settings.relay_config['port'], debug=1)

# where to listen for incoming messages
settings.receiver = SMTPReceiver(settings.receiver_config['host'],
                                 settings.receiver_config['port'])

# when silent, it won't reply to emails it doesn't know
settings.silent = settings.is_silent_config

# owner email to send all unknown emails
settings.owner_email = settings.owner_email_config

# server for email
settings.server_name = settings.server_name_config

# server for website
settings.web_server_name = settings.web_server_name_config or settings.server_name_config

Router.defaults(**settings.router_defaults)
Router.load(settings.handlers)
Router.RELOAD=True
Router.UNDELIVERABLE_QUEUE=queue.Queue("run/undeliverable")
Router.FULL_QUEUE=queue.Queue("run/full")     # all mails received
Router.ERROR_QUEUE=queue.Queue("run/error")   # mails received from unknown people
Router.UPLOAD_QUEUE=queue.Queue("run/upload") # mails to add to the DB
Router.STATE_STORE=state_storage.UserStateStorage()


view.LOADER = jinja2.Environment(
    loader=jinja2.PackageLoader(settings.template_config['dir'], 
                                settings.template_config['module']),
    extensions=['jinja2.ext.i18n'])
#TODO add i18n
# see http://jinja.pocoo.org/docs/extensions/#i18n-extension
# and http://docs.python.org/2/library/gettext.html
