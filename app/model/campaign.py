from config.settings import server_name
from webapp.poissonmagique.models import Campaign, Human, Character
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from email.utils import parseaddr
import logging
import re

def find_sender(message):
    name, sender = parseaddr(message['from'])
    try:
        human = Human.objects.get(mail_address=sender)
    except Human.DoesNotExist:
        logging.debug("Unknown sender: %s", sender)
        return None
    return human

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
    

def find_campaign_for_sender(human):
    return human.campaign

def is_gm(human, campaign):
    return campaign.gm == human

    

