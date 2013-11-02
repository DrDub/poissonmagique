from lamson import queue
from lamson.routing import route, stateless
from webapp.poissonmagique.models import Campaign, Human, Character, Fragment, MessageID, Message
from webapp.poissonmagique.queue_utils import queue_push, get_message_id
from app.model.campaign import find_sender, find_campaign_for_sender, is_gm, find_recipient
import logging
from email.utils import parseaddr
from datetime import datetime


@route("(address)@(host)", address=".+")
@stateless
def START(message, address=None, host=None):
    if len(Message.objects.filter(message_id=get_message_id(message))) > 0:
        logging.debug("Ignoring message already uploaded: %s", get_message_id(message))
        return 

    human = find_sender(message)

    campaign = None
    campaign_id = message['X-Poisson-Magique-Campaign']
    if campaign_id is not None:
        try:
            campaign = Campaign.objects.get(pk=int(campaign_id))
        except Campaign.DoesNotExist:
            campaign = None
    if campaign is None:
        # re-do the searching for the campaign
        campaign = find_campaign_for_sender(human)

    # extract the text from the email

    # TODO: do something better here
    text = message.body()

    # TODO: handle file attachments

    # TODO: other recipients


    # write to the campaign logging queue
    campaign_queue = queue.Queue("run/campaign-%d" % ( campaign.id, ))
    key = campaign_queue.push(message)
    db_msg_id = queue_push(campaign_queue, message, key)
    message_id = db_msg_id.message_id

    # look for author's character, if any
    try:
        author_character = Character.objects.get(controller=human, campaign=campaign)
    except Character.DoesNotExist:
        author_character = None
    except Character.MultipleObjectsReturned:
        author_character = None

    # create base message
    # TODO: extract the time of the message for the 'when'
    db_msg = Message( message_id = message_id,
                      author_human = human,
                      author_character = author_character,
                      subject = message['Subject'],
                      campaign = campaign,
                      text = text,
                      when = datetime.now(),
                      game_time = campaign.game_time )
    db_msg.save()
    for recipient in message['To'].split(","):
        _, rcpt_address = parseaddr(recipient)
        target, character = find_recipient(rcpt_address, campaign, name='recipient')

        db_msg.receivers_human.add( target )
        if character is not None:
            db_msg.receivers_character.add( character )
            

    # TODO: check X-Must-Forward and forward appropriately 
