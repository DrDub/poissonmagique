from config.settings import relay, owner_email, silent, server_name, web_server_name
from salmon.routing import route, stateless
from email.utils import parseaddr
from datetime import datetime
from salmon.mail import MailResponse
from app.model.emails import tst_email_sent, get_message_id
import time
import logging


@route("(address)@(host)", address=".+")
@stateless
def START(message, address=None, host=None):
    if tst_email_sent(message):
        logging.debug("Ignoring message already uploaded: %s / %s",
                      message['X-Poisson-Magique-ID'], get_message_id(message))
        return 

    attempts = 0
    while attempts < 10:
        try:
            relay.send(msg)
            return
        except SMTPException as err:
            logging.debug(u"SENDER ERROR %s to %s from %s - retrying %s " %
                        (err, msg['to'], msg['from'], str(attempts)))
            time.sleep(2) # wait for 2 seconds
        attemps += 1
    logging.debug(u"SENDER ERROR %s to %s from %s - UNSENT" %
                    (err, msg['to'], msg['from'], str(attempts)))
            
