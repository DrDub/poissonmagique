import logging
from email.utils import parseaddr
from config.settings import relay, owner_email, silent, server_name, web_server_name
from salmon.routing import route, route_like, stateless, Router
from salmon.bounce import bounce_to
from salmon.mail import MailResponse
from salmon import view
from salmon.server import SMTPError
from app.model.campaign import set_bouncing, place_sender, \
     INTERNAL, UNKNOWN, campaign_name, campaign_language, \
     character_exists, new_npc, new_enrolment
from app.model.character import find_character
from app.model.dice import find_roll, set_roll_outcome
from utils.unicode_helper import safe_unicode


@route(".+")
def GM_BOUNCE(message):
    set_bouncing(message)
    

@route(".+")
def IGNORE_BOUNCE(message):
    return START

@route("pm-new-campaign@(host)")
def NEW_CAMPAIGN(message):
    return _new_campaign(message, lang='es', 'pm-new-campaign')

@route("pm-new-campaign-es@(host)")
def NEW_CAMPAIGN(message):
    return _new_campaign(message, lang='en', 'pm-new-campaign')
    
def _new_campaign(message, lang, service_address):
    
    # check if the email address is know, if it is, croak
    sender = place_sender(message)
    if sender != UNKNOWN:
        msg = "Already playing"
        if type(sender) is tuple:
            msg = msg + " " + campaign_name(sender[0])
        raise SMTPError(550, msg)
    
    # use subject for name of campaign
    campaign_name = message['subject']
    
    # create campaign, set language to lang
    cid = new_campaign(campaign_name, message['from'], lang)

    # generate reply
    attribution = get_attribution(message['from'])
    msg = view.respond(locals(), "%s/new_campaign.msg" % (lang,),
                           From="%s@%s" % (service_address, server_name),
                           To=message['from'],
                           Subject=view.render(locals(), "%s/new_campaign.subj"))

    logging.debug(u"MESSAGE to %s@%s from %s, new campaign %s - %s" %
                      (service_address, server_name,
                           safe_unicode(message['from']),
                      str(cid), campaign_name))
    relay.deliver(msg)
    return START
                       
@route("pm-register-(pc_or_npc)pc@(host)", pc_or_npc="n?")
def NEW_CHARACTER(message, pc_or_npc):
    # check the sender is an active GM, otherwise raise 550
    sender = place_sender(message)

    if sender == INTERNAL:
        return # ignore

    if sender == UNKNOWN:
        raise SMTPError(550, "Unknown sender")
    
    if not sender[1]:
        raise SMTPError(550, "Not a GM")
    cid = sender[0]
    lang = campaign_language(cid):
    campaign_name = campaign_name(cid)
    attribution = get_attribution(message['from'])
    service_address = 'pm-register-' + ("n" if pc_or_npc else "") + "-pc"

    # get name of the character from subject, produce short form,
    # ensure short form doesn't collide with existing characters
    full_name = message['from']

    if '(' in full_name:
        ( full_name, short_form ) = full_name.split('(')
        full_name = full_name.strip()
        short_from = short_form[0:-1].strip()
    else:
        short_form = full_name.split(' ')[0]
        full_name = full_name.strip()
    short_form = short_form.lower()

    if character_exists(cid, short_form):
        all_characters = all_characters(cid)
        msg = view.respond(locals(), "%s/repeated_short_form.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/repeated_short_form.subj"))

        logging.debug(u"DUPLICATE short form %s, campaign %s" %
                        (short_form, str(cid)))
        relay.deliver(msg)
        return START

    if pc_or_npc:
        # create NPC, associate it with current campaign
        new_npc(cid, short_form, full_name)

        all_characters = all_characters(cid)

        # return template on the campaign language confirming its creation
        msg = view.respond(locals(), "%s/new_npc.msg" % (lang,),
                            From="%s@%s" % (service_address, server_name),
                            To=message['from'],
                            Subject=view.render(locals(),
                                                    "%s/new_npc.subj"))

        logging.debug(u"NEW_NPC short form %s, campaign %s" %
                        (short_form, str(cid)))
        relay.deliver(msg)
        return START
    else:
        # TODO create PC, associate it with current campaign

        # TODO generate enrolment email

        # TODO return template on the campaign language with the enrolment email


# main entry point, messaging the GM/Character
@route("(address)@(host)", address="(([^p][^m][^-])|(...)|(....)).*")
@bounce_to(soft=GM_BOUNCE, hard=GM_BOUNCE)
def START(message, address=None, host=None):
    # TODO internal sender, ignore
    
    # TODO check the sender is known otherwise raise 541
    #   http://www.serversmtp.com/en/smtp-error

    # TODO check the message haven't been processed already, otherwise
    # ignore

    # TODO set the message as been processed

    # TODO determine whether the sender is a GM
    sender_is_gm = False

    if sender_is_gm:
        # TODO determine if the email is sent as somebody else
        
        send_as = None

        # TODO validate the as-XYZ is valid or note, otherwise
        if not valid_send_as:
            # TODO reply with error to the GM with list of valid send-as

            # TODO use template on the campaign language

        # TODO for each recipient that is not an NPC, generate an
        # email either from the gm or from whomever is send_as to them
        # with cc: to the other characters and send them

    else:
        # TODO change the sender to their character email and send to GM



    # OLD email GM
    
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


    # OLD handling messaging a character
    
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
        raise SMTPError(550, "We don't know you")
    
    return human
