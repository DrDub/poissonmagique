from webapp.poissonmagique.models import Campaign, Human, Character
from django.core.exceptions import ObjectDoesNoetExist

def find_sender(message):
    sender = message['from']
    try:
        human = Human.objects.get(email=sender)
    except DoesNotExist:
        logging.DEBUG("Unknown sender %", sender)
        return None

def find_campaign_for_sender(human):
    return human.campaign

def is_gm(human, campaign):
    return campaign.gm == human
