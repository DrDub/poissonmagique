import logging
from email.utils import parseaddr
from config.settings import relay, owner_email, silent, server_name, web_server_name
from salmon.routing import route, route_like, stateless, Router
from salmon.bounce import bounce_to
from salmon.mail import MailResponse
from salmon import view
from app.model.campaign import find_sender, find_recipient, find_campaign_for_sender, is_gm
from app.model.character import find_character
from app.model.dice import find_roll, set_roll_outcome
from utils.unicode_helper import safe_unicode

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
    logging.info(u"MESSAGE to gm@%s:\n%s" % (host, safe_unicode(str(message))))
    # check the sender
    human = _check_sender(message)
    if human is None:
        return

    logging.debug(u"MESSAGE to gm@%s from %s, sender %d" % (host, safe_unicode(message['from']), human.id))

    # check the campaign
    campaign = find_campaign_for_sender(human)
    if campaign is None:
        # let this person know is game over
        return NO_GAME(message)

    logging.debug(u"MESSAGE to gm@%s from %s, campaign %s" % (host, safe_unicode(message['from']), campaign.name))

    # enque for uploading
    message['X-Poisson-Magique-Campaign'] =  safe_unicode(campaign.id)
    message['X-Must-Forward'] = safe_unicode(True)

    gm = campaign.gm
    if gm == human:
        message['X-Must-Forward'] = safe_unicode(False) # we shouldn't forward, for sure
        logging.debug(u"MESSAGE to gm@%s from %s, campaign %s is from GM" % (host, safe_unicode(message['from']), campaign.name))

    Router.UPLOAD_QUEUE.push(message)

    if False: # (now handled at uploader) gm != human and not gm.is_bouncing:
        # send to the actual GM, if it is not bouncing

        # use as From the UID
        new_from = 'poisson-%d@%s' % (human.user.id, server_name,)
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
@route("(address)@(host)", address="(([^r][^o][^l][^l][^-])|(...)|(....)).*")
def START(message, address=None, host=None):
    human = _check_sender(message)
    if human is None:
        # TODO determine which adventure this player is or just log it
        return

    # check the campaign
    campaign = find_campaign_for_sender(human)
    if campaign is None:
        # let this person know is game over
        return NO_GAME(message)

    gm = campaign.gm

    if human == gm:
        logging.info(u"MESSAGE from gm to %s@%s:\n%s" % (address, host, safe_unicode(str(message))))
        # enque for uploading
        message['X-Poisson-Magique-Campaign'] = unicode(campaign.id)
        message['X-Must-Forward'] = unicode(True)
        Router.UPLOAD_QUEUE.push(message)

        if False: # now handled at uploader
            from_gm = 'gm@%s' % (server_name,)
            for recipient in message['To'].split(","):
                _, rcpt_address = parseaddr(recipient)
                target, _ = find_recipient(rcpt_address, campaign, name='recipient')

                # TODO: check if the GM is allowed to message this human
                # TODO: move this to the upload queue, there's no way to avoid double-forwarding for multiple to:

                if target is not None:
                    new_message = MailResponse(To=target.mail_address, From=from_gm, 
                                               Subject=message['Subject'],
                                               Body=message.body())
                    new_message.attach_all_parts(message)
                    new_message['X-Poisson-Magique'] = 'This is fictious email for a game, see http://%s for details.' % ( server_name,)

                    relay.deliver(new_message)
    else: # PC-to-PC
        # enque for uploading
        logging.info(u"MESSAGE to %s@%s:\n%s" % (address, host, safe_unicode(str(message))))

        message['X-Poisson-Magique-Campaign'] = unicode(campaign.id)
        message['X-Must-Forward'] = unicode(True)
        Router.UPLOAD_QUEUE.push(message)

@route_like(START)
@bounce_to(soft=IGNORE_BOUNCE, hard=IGNORE_BOUNCE)
def NO_GAME(message, host=None):
    no_game = view.respond(locals(), "no_game.msg",
                           From=owner_email,
                           To=message['from'],
                           Subject="You're not playing a game in this server.")
    logging.debug(u"MESSAGE to gm@%s from %s, unknown campaign" % (host, safe_unicode(message['from'])))
    relay.deliver(no_game)
    return START # reset

def _check_sender(message):
    human = find_sender(message)
    if human is None:
        # unknown person
        logging.debug(u"MESSAGE to %s from %s, unknown sender" % (safe_unicode(message['to']), safe_unicode(message['from'])))
        if silent:
            #TODO log to unknown sender queue
            return None
        else:
            #TODO go to a "send informational message saying we don't know you"
            return None

    return human
