import logging
from config.settings import owner_email, silent, server_name_config, relay
from salmon.routing import route, route_like, stateless, Router
from salmon import view
from app.model.unicode_helper import safe_unicode
from salmon.bounce import bounce_to
from salmon.mail import MailResponse
from salmon.server import SMTPError
from app.model.emails import tst_email_processed, send_or_queue, sanitize
import app.model.campaign as c
from app.model.campaign import INTERNAL, UNKNOWN
from app.model.dice import find_roll, execute_roll, add_roll, RollStrParseException


@route("pm-dice-(rollid)@(host)", rollid="\d+")
@stateless
def DICE(message, rollid, host=None):
    service_address = 'pm-dice-' + rollid
    server_name = server_name_config

    # check the sender is known
    sender = place_sender(message)
    if sender == INTERNAL:
        logging.debug(u"INTERNAL ignoring %s@%s from %s" %
                      (service_address, server_name, message['from']))
        return # ignore    
    if sender == UNKNOWN:
        if silent:
            logging.debug(u"UNKNOWN ignoring %s@%s from %s" %
                      (service_address, server_name, message['from']))
            return
        raise SMTPError(550, "Unknown sender")

    cid = sender[0]
    lang = c.campaign_language(cid)

    # verify the rollid exists and belongs to the sender
    roll_obj = find_roll(rollid)

    if roll_obj is None:
        # croak no roll
        msg = view.respond(locals(), "%s/roll/no_roll.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/no_roll.subj" % (lang,)))        
        send_or_queue(msg, cid)
        return
    if roll_obj is True:
        # croak already rolled, return result
        ( roll, check, roll_str ) = execute_roll(rollid)
        msg = view.respond(locals(), "%s/roll/already_rolled.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/already_rolled.subj" % (lang,)))
        send_or_queue(msg, cid)
        return

    ( roll_cid, roll_character, roll_str ) = roll_obj

    if str(roll_cid) != str(cid):
        # croak spurious ID
        msg = view.respond(locals(), "%s/roll/no_roll.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/no_roll.subj" % (lang,)))
        send_or_queue(msg, cid)
        return
    
    if not sender[1] and str(character) != sender[2]:
        # croak not the right person for this roll
        msg = view.respond(locals(), "%s/roll/wrong_person.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/wrong_person.subj" % (lang,)))
        send_or_queue(msg, cid)
        return

    # perform the roll
    ( roll, check ) = execute_roll(rollid)

    # report back to the sender and GM (if they are different)
    (gm_address, gm_full, attribution) = c.campaign_gm(cid)

    # GM email
    msg = view.respond(locals(), "%s/roll/rolled.msg" % (lang,),
                           From="%s@%s" % (service_address, server_name,),
                           To=gm_full,
                           Subject=view.render(locals(),
                                                   "%s/roll/rolled.subj"  % (lang,)))
    if not sender[1]:
        msg['cc'] = '%s@%s' % (roll_character, server_name,)
        
    send_or_queue(msg, cid)

    if not sender[1]:
        character = c.get_character(cid, roll_character)
        attribution = c.get_attribution(character['controller'])
        
        msg = view.respond(locals(), "%s/rolled.msg" % (lang,),
                               From="%s@%s" % (service_address, server_name,),
                               To= formataddr( (attribution, character['controller']) ),
                               Subject=view.render(locals(),
                                                       "%s/rolled.subj"  % (lang,)))
        msg['cc'] = 'gm@%s' % (server_name,)
        send_or_queue(msg, cid)
        
    return
        
    

@route("pm-roll@(host)")
@stateless
def ROLL(message, host=None):
    service_address = 'pm-roll'
    sender = c.place_sender(message)
    if sender == INTERNAL:
        return # ignore    
    if sender == UNKNOWN:
        if silent:
            return
        raise SMTPError(550, "Unknown sender")
    
    if not sender[1]:
        # croak only GMs can ask for rolls
        msg = view.respond(locals(), "%s/roll/not_gm.msg" % (lang,),
                               From="%s@%s" % (service_address, server_name,),
                               To=message['from'],
                               Subject=view.render(locals(),
                                                    "%s/roll/not_gm.subj"  % (lang,)))
        send_or_queue(msg, cid)
        return
    
    (gm_address, gm_full, attribution) = c.campaign_gm(cid)

    # find the recipient that is a PC (if none, internal roll from the GM)
    recipients = c.get_recipients(message)
    character = None
    for recipient in recipients:
        if recipient == 'gm':
            continue
        this_character = c.get_character(cid, recipient)
        if not this_character['is_npc']:
            if character is not None:
                # croak only one character per roll
                msg = view.respond(locals(), "%s/roll/too_many_characters.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name,),
                            To=gm_full,
                            Subject=view.render(locals(),
                                                   "%s/roll/too_many_characters.subj"  % (lang,)))
                send_or_queue(msg, cid)
                return
            character = recipient

    # find the roll commands
    rolls = []
    full_content = message.body()
    text = safe_unicode(full_content)
    lines = text.split('\n')
    for line in lines:
        if line.startswith('ROLL:'):
            rolls.append(line[len('ROLL:'):])
    if len(rolls) == 0:
        # croak no rolls
        msg = view.respond(locals(), "%s/roll/no_rolls.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name,),
                            To=gm_full,
                            Subject=view.render(locals(),
                                                   "%s/roll/no_rolls.subj"  % (lang,)))
        send_or_queue(msg, cid)
        return

    # for each roll command, register a roll-id and send a pm-dice-(rollid) email
    if character is not None:
        character = c.get_character(cid, character)
        attribution = c.get_attribution(character['controller'])
     
    for roll in rolls:
        try:
            hashid = add_roll( cid, 'gm' if character is None else character, roll )
            service_address = 'pm-dice-' + rollid

            msg = view.respond(locals(), "%s/roll/to_roll.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name,),
                            To=gm_full if character is None else character['controller'],
                            Subject=view.render(locals(),
                                                   "%s/roll/to_roll.subj"  % (lang,)))
        except RollStrParseException as e:
            msg = view.respond(locals(), "%s/roll/syntax_error.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name,),
                            To=gm_full,
                            Subject=view.render(locals(),
                                                   "%s/roll/syntax_error.subj"  % (lang,)))
        send_or_queue(msg, cid)
    return

    
