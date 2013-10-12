import logging
from lamson.routing import route, route_like, stateless
from config.settings import relay, owner_email, silent
from lamson import view
from app.models.campaign import find_sender, find_campaign_for_sender, is_gm


# main entry point, messaging the GM
@route("gm@(host)")
def START(message, host=None):
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
    
    #TODO send to the actual GM, if it is not bouncing

    #TODO unknown GM, send it owner, if any

    
@route(".+")
def GM_BOUNCE(message):
    #TODO mark GM as bouncing
    pass

# secondary entry point, messaging a character
@route("(address)@(host)", address=".+")
def START(message, address=None, host=None):
    # TODO determine which adventure this player is or just log it
    # create the entry as a pending message and die off

@route_like(START)
def NO_GAME(message):
    #TODO say you're currently playing no game in this server
