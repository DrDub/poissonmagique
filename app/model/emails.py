from config.settings import server_name
from email.utils import parseaddr, formataddr
import table as t

# data model:

# msg-%id -> 1
# campaign-%cid-emails -> [ %id ]

def tst_email_processed(message, cid):
    msgid = message['Message-ID']
    key = 'msg-%s' % (msgid,)
    if t.has_key(key):
        return True
    t.set_key(key, 1)
    t.add_to_list('campaign-%s-emails' % (str(cid),), msgid)
    return False
