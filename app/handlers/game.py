import logging
from config.settings import relay, owner_email, silent, server_name, web_server_name
from lamson.routing import route, route_like, stateless, Router
from lamson.bounce import bounce_to
from lamson.mail import MailResponse
from lamson import view
from app.model.campaign import find_sender, find_campaign_for_sender, is_gm, find_human
from app.model.character import find_character


@route(".+")
def GM_BOUNCE(message):
    # mark GM as bouncing
    human = find_sender(message.bounce.final_recipient)
    human.is_bouncing = True
    human.save()

@route(".+")
def IGNORE_BOUNCE(message):
    return START

# main entry point, messaging the GM
@route("gm@(host)")
@bounce_to(soft=GM_BOUNCE, hard=GM_BOUNCE)
def START(message, host=None):
    logging.info("MESSAGE to gm@%s:\n%s" % (host, str(message)))
    # check the sender
    human = _check_sender(message)
    if human is None:
        return

    logging.debug("MESSAGE to gm@%s from %s, sender %d" % (host, str(message['from']), human.id))

    # check the campaign
    campaign = find_campaign_for_sender(human)
    if campaign is None:
        # let this person know is game over
        return NO_GAME(message)

    logging.debug("MESSAGE to gm@%s from %s, campaign %s" % (host, str(message['from']), campaign.name))

    # enque for uploading
    message['X-Poisson-Magique-Campaign'] = str(campaign.id)
    message['X-Must-Forward'] = str(False) # change to True to enable forwarding on uploader queue

    gm = campaign.gm
    if gm == human:
        message['X-Must-Forward'] = str(False) # we shouldn't forward, for sure
        logging.debug("MESSAGE to gm@%s from %s, campaign %s is from GM" % (host, str(message['from']), campaign.name))

    Router.UPLOAD_QUEUE.push(message)

    if gm != human and not gm.is_bouncing:
        # send to the actual GM, if it is not bouncing

        # use as From an encoded version of the human email
        # TODO: add a privacy setting that could replace this with 'user-%d' % (user.id,) instead
        new_from = '%s@%s' % (human.mail_address.replace('@','%'), server_name,)
        # find their character and use it as From, if any
        character = find_character(human)
        if character is not None:
            new_from = "%s <%s>" % (character.name, character.mail_address)

        msg_id = message['Message-ID'][1:-1]
        new_message = MailResponse(To=gm.mail_address, From=new_from, 
                                   Subject=message['Subject'],
                                   Body="Original sender: %s.\nSee it online at http://%s/msg/%s.\n\n%s" % (
                human.mail_address, web_server_name, msg_id, "" if message.base.parts else message.body()))
        new_message.attach_all_parts(message)
        new_message['X-Poisson-Magique'] = 'This is fictious email for a game, see http://%s for details.' % ( server_name,)

        relay.deliver(new_message)
    
# secondary entry point, messaging a character
@route("(address)@(host)", address=".+")
def START(message, address=None, host=None):
    # TODO determine which adventure this player is or just log it
    human = _check_sender(message)
    if human is None:
        return

    # check the campaign
    campaign = find_campaign_for_sender(human)
    if campaign is None:
        # let this person know is game over
        return NO_GAME(message)

    gm = campaign.gm

    if human == gm:
        logging.info("MESSAGE from gm to %s@%s:\n%s" % (address, host, str(message)))
        # enque for uploading
        message['X-Poisson-Magique-Campaign'] = str(campaign.id)
        message['X-Must-Forward'] = str(False) # change to True to enable forwarding on uploader queue
        Router.UPLOAD_QUEUE.push(message)

        from_gm = 'gm@%s' % (server_name,)
        for recepient in message['To']:
            target = find_human(recepient)

            if target is not None:
                new_message = MailResponse(To=target.mail_address, From=from_gm, 
                                           Subject=message['Subject'],
                                           Body=message.body())
                new_message.attach_all_parts(message)
                new_message['X-Poisson-Magique'] = 'This is fictious email for a game, see http://%s for details.' % ( server_name,)

                relay.deliver(new_message)
    else: # TODO: PC-to-PC
        # create the entry as a pending message and die off
        logging.debug("MESSAGE to %s@%s MISSING:\n%s" % (address, host, str(message)))

@route_like(START)
@bounce_to(soft=IGNORE_BOUNCE, hard=IGNORE_BOUNCE)
def NO_GAME(message, host=None):
    no_game = view.respond(locals(), "no_game.msg",
                           From=owner_email,
                           To=message['from'],
                           Subject="You're not playing a game in this server.")
    logging.debug("MESSAGE to gm@%s from %s, unknown campaign" % (host, str(message['from'])))
    relay.deliver(no_game)
    return START # reset

def _check_sender(message):
    human = find_sender(message)
    if human is None:
        # unknown person
        logging.debug("MESSAGE to gm@%s from %s, unknown sender" % (host, str(message['from'])))
        if silent:
            #TODO log to unknown sender queue
            return None
        else:
            #TODO go to a "send informational message saying we don't know you"
            return None

    return human
