from webapp.poissonmagique.models import Campaign, Human, Character
from django.core.exceptions import ObjectDoesNotExist
from email.utils import parseaddr
import logging

def find_sender(message):
    name, sender = parseaddr(message['from'])
    try:
        human = Human.objects.get(mail_address=sender)
    except ObjectDoesNotExist:
        logging.debug("Unknown sender %s", sender)
        return None
    return human

def find_campaign_for_sender(human):
    return human.campaign

def is_gm(human, campaign):
    return campaign.gm == human

