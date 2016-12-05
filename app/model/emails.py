from config.settings import relay, owner_email, silent, server_name_config
from smtplib import SMTPException
from salmon.routing import route, route_like, stateless, Router
from email.utils import parseaddr, formataddr
import table as t
import logging

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
    sent_id = increment('msg-sent')
    msg['X-Poisson-Magique-Campaign'] = str(cid)
    msg['X-Poisson-Magique-ID'] = str(sent_id)
    try:
        relay.send(msg)
        tst_email_sent(msg)
    except SMTPException as err:
        logging.debug(u"SENDER ERROR %s to %s from %s - enqueing" %
                      (err, msg['to'], msg['from']))
    Router.SENDER_QUEUE.push(msg)
        
def get_message_id(msg):
    return msg['Message-ID'][1:-1]

