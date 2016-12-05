from config.settings import relay, owner_email, silent, server_name_config
from smtplib import SMTPException
from salmon.routing import route, route_like, stateless, Router
from email.utils import parseaddr, formataddr
from app.model.unicode_helper import safe_unicode
import table as t
import logging
import re

# data model:

# msg-%id -> 1
# campaign-%cid-emails -> [ %id ]

# msg-sent -> counter id

def tst_email_processed(message, cid):
    msgid = message['Message-Id']
    key = 'msg-%s' % (msgid,)
    if t.has_key(key):
        return True
    t.set_key(key, 1)
    t.add_to_list('campaign-%s-emails' % (str(cid),), msgid)
    return False

def tst_email_sent(message):
    cid = message['X-Poisson-Magique-Campaign']
    msgid = 'sent-%s' % (message['X-Poisson-Magique-ID'],)
    key = 'msg-%s' % (msgid,)
    if t.has_key(key):
        return True
    t.set_key(key, 1)
    t.add_to_list('campaign-%s-emails' % (str(cid),), msgid)
    return False

def send_or_queue(msg, cid):
    sent_id = t.increment('msg-sent')
    msg['X-Poisson-Magique-Campaign'] = str(cid)
    msg['X-Poisson-Magique-ID'] = str(sent_id)
    try:
        relay.deliver(msg)
        tst_email_sent(msg)
    except SMTPException as err:
        logging.debug(u"SENDER ERROR %s to %s from %s - enqueing" %
                      (err, msg['to'], msg['from']))
    Router.SEND_QUEUE.push(msg)
        
def get_message_id(msg):
    return msg['Message-ID'][1:-1]

def sanitize(body_text):
    """Drop PM signature, delete email names"""
    text = safe_unicode(body_text)
    lines = text.split('\n')
    new_text = ""
    for line in lines:
        if line == "--------------------------------------------------":
            # beginning of footer, drop rest
            break
        cleaned_line = "[EMAIL]".join(re.split("[A-Za-z0-9\.\_\+\-]+\@[A-Za-z0-9\_\-]+\.[A-Za-z0-9\.\-]+", line))
        new_text = new_text + cleaned_line + "\n"
    return new_text
