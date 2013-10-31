from lamson import queue
from lamson.routing import route, stateless
from webapp.poissonmagique.models import Campaign, Human, Character, Fragment, MessageID,
from webapp.poissonmagique.queue_utils import queue_push
import logging


@route("(address)@(host)", address=".+")
@stateless
def START:
    human = find_sender(message)

    try:
        campaign = Campaign.objects.get(pk=int(message['X-Poisson-Magique-Campaign']))
    except Campaign.DoesNotExist:
        # re-do the searching for the campaign
        campaign = find_campaign_for_sender(human)

    # extract the text from the email

    # TODO: do something better here
    text = message.body()

    # TODO: handle file attachments

    # TODO: other recipients


    # write to the campaign logging queue
    queue = queue.Queue("run/campaign-%d" % ( campaign.id, ))
    key = queue.push(message)
    db_msg_id = queue_push(queue, message, key)
    message_id = db_msg_id.message_id
    
    # TODO author_character, receivers_human
    db_msg = Message( message_id = message_id,
                      author_human = human,
                      receivers_hyman = [ campaign.gm ] )
    db_msg.save()
