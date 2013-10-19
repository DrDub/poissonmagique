import logging
from lamson.routing import route, route_like, stateless
from lamson.bounce import bounce_to
from config.settings import relay, owner_email, silent, server_name
from lamson import view
from app.model.campaign import find_sender, find_campaign_for_sender, is_gm
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
    logging.info("MESSAGE to %s@%s:\n%s" % (to, host, str(message)))
    # check the sender
    human = find_sender(message)
    if human is None:
        # unknown person
        if silent:
            #TODO log to unknown sender queue
            pass
        else:
            #TODO go to a "send informational message saying we don't know you"
            pass

    # check the campaign
    campaign = find_campaign_for_sender(human)
    if campaign is None:
        # let this person know is game over
        return NO_GAME

    # enque for uploading
    Router.UPLOAD_QUEUE.push(message)

    gm = campaign.gm
    if gm != human and not gm.is_bouncing:
        # send to the actual GM, if it is not bouncing
        msg_id = message['Message-ID']
        message.epiloge = "See it online at <a href='http://%s/msg/%s'>%s/msg/%s</a>." % (
            server_name, msg_id, server_name, msg_id )
        message.add_header('X-Poisson-Magique', 'This is fictious email for an game, see %s for details' % (
                server_name,))
        message['to'] = gm.mail_address
        # find their character
        character = find_character(human)
        if character is None:
            message['form'] = 'gm@%s' % (server_name,)
        else:
            message['from'] = character.mail_address
        relay.deliver(message)
    
# secondary entry point, messaging a character
@route("(address)@(host)", address=".+")
def START(message, address=None, host=None):
    # TODO determine which adventure this player is or just log it
    # create the entry as a pending message and die off
    pass

@route_like(START)
@bounce_to(soft=IGNORE_BOUNCE, hard=IGNORE_BOUNCE)
def NO_GAME(message):
    no_game = view.respond(locals(), "no_game.msg",
                           From="noreply@%(host)s",
                           To=message['from'],
                           Subject="You're not playing a game in this server.")
    relay.deliver(no_game)
