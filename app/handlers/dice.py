import logging
from config.settings import relay, server_name, web_server_name
from lamson.routing import route
from lamson import view
from app.model.character import find_character
from app.model.dice import find_roll, set_roll_outcome
from utils.unicode_helper import safe_unicode

# dice entry point
@route("roll-(hashid)@(host)", hashid="[0-9]+")
def START(message, hashid=None, host=None):
    hashid = int(hashid)
    roll = find_roll(hashid)
    if roll is None:
        logging.info("Unknown roll %d" % (hashid))
        return

    outcome = message.body()
    set_roll_outcome(roll, outcome)
    logging.debug(u"Roll %d outcome for %s:\n%s" % (hashid, unicode(roll.target), outcome))

    # notify GM
    if not roll.campaign.gm.is_bouncing:
        character = find_character(roll.target, roll.campaign)
        mail = 'gm@%s' % (host,)
        
        if character is None:
            mail = 'poisson-%d@%s' % (roll.target.user.id, server_name,)
            character = safe_unicode(roll.target)
        else:
            mail = character.mail_address
            character = safe_unicode(character)
            
        outcome = safe_unicode(outcome)
        dice = view.respond(locals(), "dice.msg",
                               From=mail,
                               To=roll.campaign.gm.mail_address,
                               Subject=message['subject']
                               )
        relay.deliver(dice)
    return START
