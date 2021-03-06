from config.settings import server_name_config
from email.utils import parseaddr, formataddr, getaddresses
from emails import purge_pc_emails
import table as t
import logging
import re
import hashlib
import random

# data model:

# campaign-counter -> int

# ext-email-%email-campaign -> campaign id
# ext-email-%email-character -> %localpart
# ext-email-%email-is-gm -> true (other undefined)
# ext-email-%email-bouncing -> true (other undefined)
# ext-email-%email-attribution -> string (full name)

# campaign-%cid -> object ( gm: %email, name: %name, language: %lang )
# campaign-%cid-characters -> list of %localpart ("Alice", etc)
# character-%cid-%localpart -> object ( name: %fullname,
#    address: %localpart, controller: email, is_npc: "1/0",
#    enrollment: %nonce, unenrollment: %nonce, alt_attribution: string )
# enrollment-%nonce -> object( campaign: %cid, character: %locapart )
# unenrollment-%nonce -> object( campaign: %cid, character: %locapart )

UNKNOWN = "UNKNOWN"
INTERNAL = "INTERNAL"

def set_bouncing(message):
    # don't know what to do with this ATM
    name, sender = parseaddr(message['from'])
    t.set_key("ext-email-%s-bouncing" % (sender,), 1)

def is_internal(address):
    (local_part, domain) = address.split('@')
    return domain == server_name_config

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

def get_recipients(message):
    """Returns a list of raw localparts for local email addresses, to:
    and cc: concatenated. Ignores external emails.
    """
    def get_all(key):
        _all = message[key]
        if  _all is None:
            return []
        if type(_all) is not list:
            return [ _all ]
        
    tos = get_all('to')
    ccs = get_all('cc')
    resent_tos = get_all('resent-to')
    resent_ccs = get_all('resent-cc')
    all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)
    addresses = map(lambda x:x[1], all_recipients)
    result = []
    for address in addresses:
        (localpart, domain) = address.split('@')
        if domain == server_name_config:
            result.append(localpart.lower())
    return result
    
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
    if not t.has_key("ext-email-%s-campaign" % (address,)):
        return UNKNOWN
    cid = t.get("ext-email-%s-campaign" % (address,))
    if t.has_key("ext-email-%s-is-gm" % (address,)):
        return ( cid, True, None )
    return ( cid, False, t.get("ext-email-%s-character" % (address,)) )

def campaign_name(cid):
    return t.get_field("campaign-%s" % (str(cid),), "name")

def campaign_language(cid):
    return t.get_field("campaign-%s" % (str(cid),), "language")

def campaign_gm(cid):
    """ email address, full email header, attribution"""
    gm_address = t.get_field("campaign-%s" % (str(cid),), "gm")
    gm_attribution = t.get('ext-email-%s-attribution' % (gm_address,))
    return ( gm_address, formataddr( (gm_attribution, gm_address) ), gm_attribution )

def new_campaign(campaign_name, full_from, language):
    name, sender = parseaddr(full_from)
    cid = t.increment('campaign-counter')

    t.set_key('ext-email-%s-campaign' % (sender,), cid)
    t.set_key('ext-email-%s-is-gm' % (sender,), 1)
    t.delete_key('ext-email-%s-bouncing' % (sender,))
    t.set_key('ext-email-%s-attribution' % (sender,), name)

    t.create_object('campaign-%s' % (str(cid),), gm=sender, name=campaign_name, language=language)

    return cid
    
def get_attribution(full_from):
    name, sender = parseaddr(full_from)
    attribution = t.get('ext-email-%s-attribution' % (sender,))
    if attribution:
        return attribution
    if name:
        t.set_key('ext-email-%s-attribution' % (sender,), name)
        
    return name

def set_attribution(full_from, new_attribution):
    name, sender = parseaddr(full_from)
    t.set_key('ext-email-%s-attribution' % (sender,), new_attribution)
    return new_attribution

def character_exists(cid, short_form):
    return t.has_key('character-%s-%s' % (str(cid), short_form))

def all_characters(cid):
    """Returns a list of dictionaries with keys 
    name, address, controller, is_npc"""

    short_forms = t.list_elems('campaign-%s-characters' % (str(cid),))
    result = []
    for short_form in short_forms:
        result.append(t.get_object('character-%s-%s' % (str(cid), short_form)))
    return result

def get_character(cid, short_form):
    """Returns a dictionary with keys name, address, controller, is_npc"""
    
    key ='character-%s-%s' % (str(cid), short_form.lower())
    if t.has_key(key):
        return  t.get_object(key)
    return None

def new_npc(cid, short_form, full_name):
    short_form = short_form.strip().lower()
    cid = str(cid)
    t.list_append('campaign-%s-characters' % (cid,), short_form)
    t.create_object( 'character-%s-%s' %(cid,short_form),
                         name=full_name,
                         address=short_form,
                         controller=t.get_field('campaign-%s' % (cid,), 'gm'),
                         is_npc=1 )
    return short_form
    
def new_pc(cid, short_form, full_name):
    short_form = short_form.strip().lower()
    cid = str(cid)

    while True:
        nonce = hashlib.sha256("%s-%s-%d" %
                                   (cid, short_form,
                                        random.randint(0,9001))).hexdigest()[0:10]
        enrollment_key = 'enrollment-%s' % (nonce,)
        if not t.has_key(enrollment_key):
            break

    t.create_object(enrollment_key, campaign=cid, character=short_form)
    
    t.list_append('campaign-%s-characters' % (cid,), short_form)
    t.create_object( 'character-%s-%s' %(cid,short_form),
                         name=full_name,
                         address=short_form,
                         is_npc=0,
                         enrollment=nonce )
    return nonce

def find_enrollment(nonce):
    return find_nonce('enrollment', nonce)

def find_unenrollment(nonce):
    return find_nonce('unenrollment', nonce)

def find_nonce(nonce, what):
    key = '%s-%s' % (what, nonce,)
    if not t.has_key(key):
        return None

    obj = t.get_object(key)

    return obj['campaign'], obj['character']

def do_enrollment(cid, nonce, full_from, short_form):
    enrollment_key = 'enrollment-%s' % (nonce,)
    t.delete_key(enrollment_key)

    (name, email) = parseaddr(full_from)

    t.set_field('character-%s-%s' % (cid, short_form), 'controller', email)
    t.set_key('ext-email-%s-attribution' % (email,), name)
    t.delete_key('ext-email-%s-bouncing' % (email,))
    t.delete_key('ext-email-%s-is-gm' % (email,))
    t.set_key('ext-email-%s-character' % (email,), short_form)
    t.set_key('ext-email-%s-campaign' % (email,), cid)

def start_unenrollment(cid, short_form):
    while True:
        nonce = hashlib.sha256("%s-%s-%d" %
                                   (cid, short_form,
                                        random.randint(0,9001))).hexdigest()[0:10]
        unenrollment_key = 'unenrollment-%s' % (nonce,)
        if not t.has_key(unenrollment_key):
            break

    t.create_object(unenrollment_key, campaign=cid, character=short_form)
    t.set_field('character-%s-%s' %(cid,short_form), 'unenrollment', nonce)

    return nonce
    

def do_unenrollment(cid, nonce):
    unenrollment_key = 'unenrollment-%s' % (nonce,)
    unenrollment = t.get_object(unenrollment_key)
    t.delete_key(unenrollment_key)

    cid = unenrollment['campaign']
    short_form = unenrollment['character']
    
    character_key = 'character-%s-%s' % (cid, short_form)
    email = t.get_field(character_key, 'controller')
    attribution = t.get_key('ext-email-%s-attribution' % (email,))
    t.set_field(character_key, 'controller', t.get_field('campaign-%s' % (cid,), 'gm'))
    t.set_field(character_key, 'is_npc', 1)
    t.set_field(character_key, 'alt_attribution', attribution)

    t.delete_key('ext-email-%s-campaign' % (email,))
    t.delete_key('ext-email-%s-character' % (email,))
    t.delete_key('ext-email-%s-bouncing' % (email,))
    t.delete_key('ext-email-%s-attribution' % (email,))

    purge_pc_emails(email)

def delete_campaign(cid):
    emails_to_delete = list()
    gm_email = t.get_field('campaign-%s' % (cid,), 'gm')
    t.delete_key('campaign-%s' % (cid,))
    emails_to_delete.append(gm_email)

    short_forms = t.list_elems('campaign-%s-characters' % (str(cid),))
    t.delete_key('campaign-%s-characters')

    for short_form in short_forms:
        character_key = 'character-%s-%s' % (str(cid), short_form)
        character = t.get_object(character_key)
        t.delete_key(character_key)
        if 'enrollment' in character:
            t.delete_key('enrollment-%s' % character['enrollment'])
        if 'unenrollment' in character:
            t.delete_key('unenrollment-%s' % character['unenrollment'])
        if not int(character['is_npc']):
            emails_to_delete.append(character['controller'])

    for email in emails_to_delete:
        t.delete_key('ext-email-%s-campaign' % (email,))
        t.delete_key('ext-email-%s-character' % (email,))
        t.delete_key('ext-email-%s-is-gm' % (email,))
        t.delete_key('ext-email-%s-bouncing' % (email,))
        t.delete_key('ext-email-%s-attribution' % (email,))
