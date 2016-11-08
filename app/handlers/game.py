import logging
from email.utils import parseaddr, formataddr
from config.settings import relay, owner_email, silent, server_name_config
from salmon.routing import route, route_like, stateless, Router
from salmon.bounce import bounce_to
from salmon.mail import MailResponse
from salmon import view
from salmon.server import SMTPError
from app.model.emails import tst_email_processed
import app.model.campaign as c
from app.model.campaign import INTERNAL, UNKNOWN
from app.model.dice import find_roll, set_roll_outcome
from utils.unicode_helper import safe_unicode

#@route(".+")
#def GM_BOUNCE(message):
#    c.set_bouncing(message)
    
#@route(".+")
#def IGNORE_BOUNCE(message):
#    return START

@route("pm-new-game@(host)")
@stateless
def NEW_CAMPAIGN(message, host=None):
    return _new_campaign(message, 'en', 'pm-new-game')

@route("pm-new-game-es@(host)")
@stateless
def NEW_CAMPAIGN_ES(message, host=None):
    return _new_campaign(message, 'es', 'pm-new-game-es')
    
def _new_campaign(message, lang, service_address):
    
    # check if the email address is know, if it is, croak
    sender = c.place_sender(message)
    if sender == INTERNAL:
        return # ignore
    if sender != UNKNOWN:
        msg = "Already playing"
        if type(sender) is tuple:
            msg = msg + " " + c.campaign_name(sender[0])
        if silent:
            logging.debug(u"MESSAGE to %s@%s from %s - already playing" %
                      (service_address, server_name, message['from']))
            return
        raise SMTPError(550, msg)
    
    # use subject for name of campaign
    campaign_name = message['subject']
    server_name = server_name_config
    
    # create campaign, set language to lang
    cid = c.new_campaign(campaign_name, message['from'], lang)

    # generate reply
    attribution = c.get_attribution(message['from'])
    msg = view.respond(locals(), "%s/new_campaign.msg" % (lang,),
                           From="%s@%s" % (service_address, server_name),
                           To=message['from'],
                           Subject=view.render(locals(),
                                               "%s/new_campaign.subj"  % (lang,)))

    logging.debug(u"MESSAGE to %s@%s from %s, new campaign %s - %s" %
                      (service_address, server_name,
                           safe_unicode(message['from']),
                      str(cid), campaign_name))
    relay.deliver(msg)
    return
                       
@route("pm-register-(pc_or_npc)pc@(host)", pc_or_npc="n?")
@stateless
def NEW_CHARACTER(message, host=None, pc_or_npc="n"):
    service_address = 'pm-register-' + ("n" if pc_or_npc else "") + "pc"
    server_name = server_name_config
    
    # check the sender is an active GM, otherwise raise 550
    sender = c.place_sender(message)
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
    
    if not sender[1]:
        if silent:
            logging.debug(u"NOT_GM ignoring %s@%s from %s" %
                      (service_address, server_name, message['from']))
            return
        raise SMTPError(550, "Not a GM")
    cid = sender[0]
    lang = c.campaign_language(cid)
    campaign_name = c.campaign_name(cid)
    attribution = c.get_attribution(message['from'])

    # get name of the character from subject, produce short form,
    # ensure short form doesn't collide with existing characters
    full_name = message['subject']

    if '(' in full_name:
        ( full_name, short_form ) = full_name.split('(')
        full_name = full_name.strip()
        if ')' in short_form:
            short_from = short_form.split(')')[0].strip()
    else:
        short_form = full_name.split(' ')[0]
        full_name = full_name.strip()
    short_form = short_form.lower()

    if c.character_exists(cid, short_form):
        all_characters = c.all_characters(cid)
        msg = view.respond(locals(), "%s/repeated_short_form.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/repeated_short_form.subj"  % (lang,)))

        logging.debug(u"DUPLICATE short form %s, campaign %s" %
                        (short_form, str(cid)))
        relay.deliver(msg)
        return

    if pc_or_npc:
        # create NPC, associate it with current campaign
        c.new_npc(cid, short_form, full_name)
        all_characters = c.all_characters(cid)

        # return template on the campaign language confirming its creation
        msg = view.respond(locals(), "%s/new_npc.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/new_npc.subj" % (lang,)))

        logging.debug(u"NEW_NPC short form %s, campaign %s" %
                        (short_form, str(cid)))
        relay.deliver(msg)
        return
    else:
        # create PC, associate it with current campaign and generate
        # enrolment email
        enrollment_address = c.new_pc(cid, short_form, full_name)
        all_characters = c.all_characters(cid)

        # return template on the campaign language with the enrollment email
        msg = view.respond(locals(), "%s/new_pc.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/new_pc.subj" % (lang,)))

        logging.debug(u"NEW_PC short form %s, enroll at %s, campaign %s" %
                        (short_form, enrollment_address, str(cid)))
        relay.deliver(msg)
        return

@route("pm-enroll-(nonce)@(host)", nonce=".+")
@stateless
def ENROLL(message, nonce, host=None):
    server_name = server_name_config
    service_address = 'pm-enroll-%s' % (nonce,)

    # check if the email address is know, if it is, croak
    sender = c.place_sender(message)
    if sender == INTERNAL:
        logging.debug(u"INTERNAL ignoring %s@%s from %s" %
                      (service_address, server_name, message['from']))        
        return # ignore    
    if sender != UNKNOWN:
        msg = "Already playing"
        if type(sender) is tuple:
            msg = msg + " " + c.campaign_name(sender[0])
        if silent:
            logging.debug(u"ALREADY ignoring %s@%s from %s - already playing" %
                      (service_address, server_name, message['from']))
            return
        raise SMTPError(550, msg)

    enrollment = c.find_enrollment(nonce)

    if enrollment is None:
        if silent:
            logging.debug(u"INVALID code, ignoring %s@%s from %s" %
                      (service_address, server_name, message['from']))
            return
        raise SMTPError(550, "Enrollment code invalid")

    (cid, short_form) = enrollment

    c.do_enrollment(cid, nonce, message['from'], short_form)

    lang = c.campaign_language(cid)
    campaign_name = c.campaign_name(cid)
    attribution = c.get_attribution(message['from'])

    msg = view.respond(locals(), "%s/enrolled_pc.msg" % (lang,),
                           From="%s@%s" % (service_address, server_name),
                           To=message['from'],
                           Subject=view.render(locals(),
                                                   "%s/enrolled_pc.subj" % (lang,)))

    logging.debug(u"ENROLLED short form %s, enrolled at %s, campaign %s" %
                      (short_form, enrollment_address, str(cid)))
    relay.deliver(msg)

    (gm_address, gm_full, attribution) = campaign_gm(cid)
    msg = view.respond(locals(), "%s/enrolled_gm.msg" % (lang,),
                           From="%s@%s" % (service_address, server_name),
                           To=gm_full,
                           Subject=view.render(locals(),
                                                   "%s/enrolled_gm.subj" % (lang,)))
    relay.deliver(msg)
    
    return
    
@route("pm-end@(host)")
@stateless
def GAME_END(message, host=None):
    sender = c.place_sender(message)
    if sender == INTERNAL:
        return # ignore    
    if sender == UNKNOWN:
        if silent:
            return
        raise SMTPError(550, "Unknown sender")
    if sender[1]:
        # TODO GM, pack and go
        sender = sender
    else:
        # TODO PC, drop to NPC and inform the GM
        sender = sender

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
    

# main entry point, messaging the GM/Character
@route("(address)@(host)", address="^[^p][^m][^-].*")
@stateless
#@bounce_to(soft=GM_BOUNCE, hard=GM_BOUNCE)
def START(message, address=None, host=None):
    if(address.startswith("pm-")):
        return # ignore
    
    sender = c.place_sender(message)
    if sender == INTERNAL:
        return # ignore    
    if sender == UNKNOWN:
        if silent:
            logging.debug(u"MESSAGE to %s@%s from %s - unknown" %
                      (address, server_name, message['from']))
            return
        raise SMTPError(550, "Unknown sender")

    cid = sender[0]
    # check the message haven't been processed already
    if tst_email_processed(message, cid):
        logging.debug(u"IGNORING processed email %s" % (message['message-id'],))
        return # ignore
    # the message as been set as processed

    lang = c.campaign_language(cid)
    campaign_name = c.campaign_name(cid)
    server_name = server_name_config    
    
    recipients = get_recipients(message)
    
    if sender[1]:
        # determine if the email is sent as somebody else
        (gm_address, gm_full, attribution) = campaign_gm(cid)
         
        send_as = None
        for recipient in recipients:
            if recipient.startswith('as-'):
                if send_as:
                    other = send_as = recipient[3:].lower()
                    msg = view.respond(locals(), "%s/repeated_as.msg" % (lang,),
                                From="gm@%s" % (server_name,),
                                To=gm_full,
                                Subject=view.render(locals(),
                                               "%s/repeated_as.subj"  % (lang,)))
                    relay.deliver(msg)
                    return
                send_as = recipient[3:].lower()

        # validate the as-XYZ is valid or note, otherwise
        if send_as:
            original_send_as = send_as
            send_as = c.get_character(cid, send_as)
        
            if not send_as:
                # reply with error to the GM with list of valid send-as
                all_characters = c.all_characters(cid)
                send_as = original_send_as
        
                msg = view.respond(locals(), "%s/unknown_as.msg" % (lang,),
                                   From="gm@%s" % (server_name,),
                                   To=gm_full,
                                   Subject=view.render(locals(),
                                                "%s/unknown_as.subj"  % (lang,)))
                relay.deliver(msg)
                return

        if send_as:
           sender = formataddr(send_as['name'],
                                   '%s@%s' % (send_as['address'],
                                                  server_name))
        else:
            sender = 'gm@%s' % (server_name,)

        # for each recipient that is not an NPC, generate an email
        # either from the gm or from whomever is send_as to them with
        # cc: to the other characters and send them
        
        # extract the text
        full_content = message.body()
        #TODO check message.base.parts
        
        for recipient in recipients:
            if recipient.startswith('as-'):
                continue
            if recipient.startswith('pm-'):
                continue
            character = c.get_character(cid, recipient)
            
            to_list = []
            for other in recipients:
                if other.startswith('as-'):
                    to_list.append('gm@%s' % (server_name,))
                if other.startswith('pm-') and not send_as:
                    # this will be ignored by the server, but notifies
                    # the users unless is a send-as which will
                    # highlight the send-as to the players
                    to_list.append('%s@%s' % (recipient, server_name))
                if other != recipient:
                    other_character = c.get_character(cid, other)
                    to_list.append(formataddr(other_character['name'],
                                                  '%s@%s' % (other,
                                                                 server_name,)))
            # sort them
            to_list = sorted(to_list)

            attribution = c.get_attribution(character['controller'])
            msg = view.respond(locals(), "%s/base.msg" % (lang,),
                                   From=sender,
                            To=formataddr(attribution, character['controller']),
                            Cc=to_list,
                            Subject=campaign_name)
    else:
        short_form = sender[2]
        full_character = c.get_character(cid, short_form)
        
        # change the sender to their character email and send to GM
        (gm_address, gm_full, attribution) = campaign_gm(cid)
        
        # cc: for show
        cc_list = []
        
        for recipient in recipients:
            if recipient == 'gm':
                continue
            character = c.get_character(cid, recipient)
            cc_list.append(formataddr(character['name'],
                                          '%s@%s' % (recipient,
                                                         server_name,)))
        # sort them
        cc_list = sorted(cc_list)

        # extract the text
        full_content = message.body()
        #TODO check message.base.parts
        msg = view.respond(locals(), "%s/base.msg" % (lang,),
                            From=formataddr(full_character['name'],
                                                "%s@%s" % (short_form, server_name)),
                            To=gm_full,
                            Cc=cc_list,
                            Subject="%s: %s" % (campaign_name, short_form))
        relay.deliver(msg)
        return

