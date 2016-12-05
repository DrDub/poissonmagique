import logging
from config.settings import relay, server_name_config
from salmon.routing import route, route_like, stateless, Router
from salmon import view
from app.model.unicode_helper import safe_unicode

@route("pm-dice-(rollid)@(host)", rollid="\d+")
@stateless
def DICE(message, rollid, host=None):
    sender = place_sender(message)
    if sender == INTERNAL:
        return # ignore    
    if sender == UNKNOWN:
        if silent:
            return
        raise SMTPError(550, "Unknown sender")

    # TODO verify the rollid exists and belongs to the sender

    # TODO perform the roll

    # TODO report back to the sender and GM (if they are different)

@route("pm-roll@(host)")
@stateless
def ROLL(message, host=None):
    sender = c.place_sender(message)
    if sender == INTERNAL:
        return # ignore    
    if sender == UNKNOWN:
        if silent:
            return
        raise SMTPError(550, "Unknown sender")
    if not sender[1]:
        if silent:
            return
        raise SMTPError(550, "Only GMs can ask for rolls")

    # TODO find the recipient that is a PC (if none, internal roll
    # from the GM)

    # TODO find the roll commands

    # TODO for each roll command, register a roll-id and send a
    # pm-dice-(rollid) email
    


# dice entry point
## @route("roll-(hashid)@(host)", hashid="[0-9]+")
## def START(message, hashid=None, host=None):
##     hashid = int(hashid)
##     roll = find_roll(hashid)
##     if roll is None:
##         logging.info("Unknown roll %d" % (hashid))
##         return

##     outcome = message.body()
##     set_roll_outcome(roll, outcome)
##     logging.debug(u"Roll %d outcome for %s:\n%s" % (hashid, unicode(roll.target), outcome))

##     # notify GM
##     if not roll.campaign.gm.is_bouncing:
##         character = find_character(roll.target, roll.campaign)
##         mail = 'gm@%s' % (host,)
        
##         if character is None:
##             mail = 'poisson-%d@%s' % (roll.target.user.id, server_name,)
##             character = safe_unicode(roll.target)
##         else:
##             mail = character.mail_address
##             character = safe_unicode(character)
            
##         outcome = safe_unicode(outcome)
##         dice = view.respond(locals(), "dice.msg",
##                                From=mail,
##                                To=roll.campaign.gm.mail_address,
##                                Subject=message['subject']
##                                )
##         relay.deliver(dice)
##     return START
