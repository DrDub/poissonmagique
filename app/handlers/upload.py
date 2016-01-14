from salmon import queue
from config.settings import relay, owner_email, silent, server_name, web_server_name
from salmon.routing import route, stateless
from webapp.poissonmagique.models import Campaign, Human, Character, Fragment, MessageID, Message
from webapp.poissonmagique.queue_utils import queue_push, get_message_id
from app.model.campaign import find_sender, find_campaign_for_sender, is_gm, find_recipient
import logging
from email.utils import parseaddr
from datetime import datetime
from salmon.mail import MailResponse


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
    if text is None:
        text = "poissonmagique: no text extracted"

    # TODO: handle file attachments

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

    # recipients
    recipients = []
    if message['To'] is not None:
        recipients += message['To'].split(",")
    if message['cc'] is not None:
        recipients += message['Cc'].split(",")
    recipients_target = []
    for recipient in recipients:
        _, rcpt_address = parseaddr(recipient)
        target, character = find_recipient(rcpt_address, campaign, name='recipient')
        recipients_target.append( (target, character) )

        db_msg.receivers_human.add( target )
        if character is not None:
            db_msg.receivers_character.add( character )

    # check X-Must-Forward and forward appropriately
    if 'X-Must-Forward' in message and message['X-Must-Forward'] == 'True':
        # the sender is (human, character), the recipients are recipients_target

        if campaign.gm == human: # if sender is gm, send to all recipients right away
            from_gm = 'gm@%s' % (server_name,)
            for recipient in recipients_target:
                target = recipient[0]
                if target != human and target is not None:
                    # TODO: check if the GM is allowed to message this human
                    new_message = MailResponse(To=target.mail_address, From=from_gm, 
                                               Subject=message['Subject'],
                                               Body=message.body())
                    new_message.attach_all_parts(message)
                    new_message['X-Poisson-Magique'] = 'This is fictious email for a game, see http://%s for details.' % ( server_name,)
                    
                    relay.deliver(new_message)
        else:
            if human != campaign.gm and not campaign.gm.is_bouncing:
                # send to the actual GM, if it is not bouncing

                # use as From the UID
                new_from = 'poisson-%d@%s' % (human.user.id, server_name,)
                # find their character and use it as From, if any
                if author_character is not None:
                    new_from = "%s <%s>" % (author_character.name, author_character.mail_address)

                msg_id = message['Message-ID'][1:-1]
                new_message = MailResponse(To=campaign.gm.mail_address, From=new_from, 
                                           Subject=message['Subject'],
                                           Body="Original sender: %s.\nSee it online at http://%s/msg/%s.\n\n%s" % (
                        human.mail_address, web_server_name, msg_id, "" if message.base.parts else message.body()))
                new_message.attach_all_parts(message)
                new_message['X-Poisson-Magique'] = 'This is fictious email for a game, see http://%s for details.' % ( server_name,)

                relay.deliver(new_message)

                # TODO indicate the rest of the recipients as PENDING for forwarding
            
        
        
