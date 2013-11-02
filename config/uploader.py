from config import settings
from lamson.routing import Router
from lamson.server import Relay, QueueReceiver
from lamson import view, queue
import logging
import logging.config
import jinja2
from app.model import state_storage

logging.config.fileConfig("config/logging.conf")

settings.receiver = QueueReceiver(settings.UPLOADER_QUEUE_PATH,
                                  settings.uploader_queue_sleep)

# when silent, it won't reply to emails it doesn't know
settings.silent = settings.is_silent_config

# owner email to send all unknown emails
settings.owner_email = settings.owner_email_config

# server for email
settings.server_name = settings.server_name_config

# server for website
settings.web_server_name = settings.web_server_name_config or settings.server_name_config

Router.defaults(**settings.router_defaults)
Router.load(settings.upload_handlers)
Router.RELOAD=True
Router.UPLOAD_QUEUE=queue.Queue(settings.UPLOADER_QUEUE_PATH) # mails to add to the DB

