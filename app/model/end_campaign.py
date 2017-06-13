from config.settings import server_name_config, campaigns_report_folder
from email.utils import parseaddr, formataddr, getaddresses, parsedate_tz, mktime_tz
from salmon.routing import Router
import table as t
import logging
import re
import os
import hashlib
import random
from campaign import all_characters, campaign_gm, get_character

def end_campaign(cid):
    """Ends a campaign, returns the list of email addresses to email,
    plus the code for downloading the log.

    It purges all emails and all information about the campaign.
    """

    full_queue = Router.FULL_QUEUE
    messages = list()

    emails_in_campaign = set()
    attribution_for_email = dict()
    ( gm_email, full_gm, gm_attribution ) = campaign_gm(cid)
    emails_in_campaign.add( gm_email )
    campaign_characters = all_characters(cid)

    for character in campaign_characters:
        if not int(character['is_npc']):
            emails_in_campaign.add(character['controller'])

    for email in emails_in_campaign:
        attribution_for_email[email] = get_attribution(email)

    for key in full_queue.keys():
        msg = full_queue.get(key)

        name, sender = parseadd(msg['From'])
        if sender in emails_in_campaign:
            msg_epoch = mktime_tz(parsedate_tz(m['Date']))
            messages.append( { 'epoch' : msg_epoch, 'msg' : msg, 'key' : key } )

    #TODO sort messages by date

    # create nonce
    while True:
        nonce = hashlib.sha256("%s-%d" %
                                   (cid, random.randint(0,9001))).hexdigest()[0:10]
        target_zip = "%s/%s.zip" % ( campaigns_report_folder, nonce ) 
        if not os.path.exists(target_zip):
            break
    os.mkdir("/tmp/" % (nonce,))
        
    #TODO front matter -- campaign name, GM, PC players, NPC players, attributions, licence.

    for t in messages:
        msg = t['msg']

        #TODO header (includes who send it, potentially as-XYZ and to/cc)

        #TODO typeset email


    #TODO end matter

    #TODO render to PDF

    #TODO zip source texts + PDF to target_zip

    # delete messages from full queue
    for t in messages:
        full_queue.remove(t['key'])

    # purge campaign from redis
    delete_campaign(cid)

    return nonce
