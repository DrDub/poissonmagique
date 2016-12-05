from config import settings
from salmon.routing import Router
from salmon.server import Relay, QueueReceiver
from salmon import view, queue
import logging
import logging.config
import jinja2
from app.model import state_storage, table

logging.config.fileConfig("config/logging.conf")

settings.receiver = QueueReceiver(settings.SENDER_QUEUE_PATH,
                                  settings.sender_queue_sleep)

# the relay host to actually send the final message to
settings.relay = Relay(host=settings.relay_config['host'], 
                       port=settings.relay_config['port'], debug=1)

# when silent, it won't reply to emails it doesn't know
settings.silent = settings.is_silent_config

# owner email to send all unknown emails
settings.owner_email = settings.owner_email_config

# server for email
settings.server_name = settings.server_name_config

# server for website
settings.web_server_name = settings.server_name_config

# start backend
table.r = table.start_table()

Router.defaults(**settings.router_defaults)
Router.load(settings.sender_handlers)
Router.RELOAD=True
Router.SEND_QUEUE=queue.Queue(settings.SENDER_QUEUE_PATH) # mails to send
Router.UNDELIVERABLE_QUEUE=queue.Queue("run/error_send")
Router.STATE_STORE=state_storage.UserStateStorage()
