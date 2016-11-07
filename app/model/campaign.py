from config.settings import server_name
from email.utils import parseaddr
import app.models.table as t
import logging
import re

# data model:

# campaign-counter -> int

# ext-email-%email-campaign -> campaign id 24
# ext-email-%email-character -> %localpart
# ext-email-%email-is-gm -> true (other undefined)
# ext-email-%email-bouncing -> true (other undefined)
# ext-email-%email-attribution -> string (full name)

# campaign-%cid -> object ( gm: %email, name: %name, language: %lang )
# campaign-%cid-characters -> list of %localpart ("Alice", etc)
# character-%cid-%localpart -> object ( name: %fullname,
#    address: %localpart, controller: email, is_npc: "t/f",
#    enrollment: "address" )
# enrolment-%customlocalpart -> object( campaign: %cid, character: %locapart )

UNKNOWN = "UNKNOWN"
INTERNAL = "INTERNAL"

def set_bouncing(message):
    # don't know what to do with this ATM
    name, sender = parseaddr(message['from'])
    t.set_key("ext-email-%s-bouncing" % (sender,), 1)

def is_internal(address):
    (local_part, domain) = address.split('@')
    return domain == server_name

def place_sender(message):
    """ 
    Determine if the sender is known.
    Returns: 
       UNKNOWN if unknown
       INTERNAL if internal
       ( %cid, True for GM or False for PC, %localpart for PC )
    """
    name, sender = parseaddr(message['from'])
    return place_address(sender)

def place_recipients(message):
    """ 
    Determine the recipients of a message
    Returns: 
       UNKNOWN if unknown
       INTERNAL if internal
       ( %cid, True for GM or False for PC, %localpart for PC )
    """
    name, sender = parseaddr(message['from'])
    return place_address(sender)

def place_address(address):
    if is_internal(address):
        return INTERNAL
    if not t.has_key("ext-email-%s-campaign"):
        return UNKNOWN
    cid = t.get("ext-email-%s-campaign")
    if t.has_key("ext-email-%s-is-gm"):
        return ( cid, True, None )
    return ( cid, False, t.get("ext-email-%s-character") )

def campaign_name(cid):
    return t.get_field("campaign-%s" % (str(cid),), "name")

def campaign_language(cid):
    return t.get_field("campaign-%s" % (str(cid),), "language")

def new_campaign(name, full_from, language):
    name, sender = parseaddr(full_from)
    cid = t.increment('campaign-counter')

    t.set_key('ext-email-%s-campaign' % (sender,), cid)
    t.set_key('ext-email-%s-is-gm' % (sender,), 1)
    t.delete_key('ext-email-%s-bouncing' % (sender,))
    t.set_key('ext-email-%s-attribution' % (sender,), name)

    t.create_object('campaign-%s' % (str(cid),), gm=sender, name=name, language=language)

    return cid
    
def get_attribution(full_from):
    name, sender = parseaddr(full_from)
    attribution = t.get('ext-email-%s-attribution' % (sender,))
    if attribution:
        return attribution
    if name:
        t.set_key('ext-email-%s-attribution' % (sender,), name)
        
    return name

def character_exists(cid, short_form):
    return t.has_key('character-%s-%s' % (str(cid), short_form))

def all_characters(cid):
    """Returns a list of dictionaries with keys 
    name, address, controller, is_npc"""

    short_forms = t.list_elems('campaign-%s-characters' % (str(cid),))
    result = []
    for short_form in short_forms:
        result.append(t.get_object('campaign-%s-%s' % (str(cid), short_form)))
    return result


########## OLD


def find_recipient(mail_address, campaign=None, name='recipient'):
    """
    Find the human behind a recipient email, either poisson-UID or character name.
    Needs a campaign ID to resolve characters
    """
    match = re.match('poisson-([0-9]+)', mail_address)
    human = ""
    if match is not None:
        uid = match.groups(0)[0]
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            logging.debug("Unknown %s: UID %d", name, uid)
            return None, None
        try:
            human = Human.objects.get(user=user)
        except Human.DoesNotExist:
            logging.debug("Unknown %s: no human for UID %d (%s)", name, uid, user.name)
            return None
        return human, None
    elif campaign is not None:
        if mail_address == "gm@%s" % (server_name,):
            return campaign.gm, None
        else:
            try:
                character = Character.objects.get(mail_address=mail_address, campaign=campaign)
                human = character.controller
                return human, character
            except Character.DoesNotExist:
                logging.debug("Unknown %s for campaign %s: %s", name, campaign.name, mail_address)
                return None, None
    else:
        logging.debug("Can't resolve %s without a campaign: %s", name, mail_address)
        return None, None
    
