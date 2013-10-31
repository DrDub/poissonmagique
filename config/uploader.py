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

Router.defaults(**settings.router_defaults)
Router.load(settings.upload_handlers)
Router.RELOAD=True
Router.UPLOAD_QUEUE=queue.Queue(settings.UPLOADER_QUEUE_PATH) # mails to add to the DB

