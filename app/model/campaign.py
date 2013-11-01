from webapp.poissonmagique.models import Campaign, Human, Character
from django.core.exceptions import ObjectDoesNotExist
from email.utils import parseaddr
import logging

def find_sender(message):
    name, sender = parseaddr(message['from'])
    return find_human(sender, 'sender')

def find_human(mail_address, name='human'):
    try:
        human = Human.objects.get(mail_address=mail_address)
    except ObjectDoesNotExist:
        logging.debug("Unknown %s: %s", name, human)
        return None
    return human

def find_campaign_for_sender(human):
    return human.campaign

def is_gm(human, campaign):
    return campaign.gm == human

