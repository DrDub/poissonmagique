from config.settings import server_name_config, campaigns_report_folder
from email.utils import parseaddr, formataddr, getaddresses, parsedate_tz, mktime_tz
from salmon.routing import Router
from salmon import view
import table as t
import logging
import re
import os
import hashlib
import random
import codecs
from subprocess import call
from campaign import all_characters, campaign_gm, get_character, campaign_language, campaign_name, get_recipients, get_attribution, place_sender
from emails import sanitize, get_message_id

def end_campaign(cid, purge=True):
    """Ends a campaign, returns the list of email addresses to email,
    plus the code for downloading the log.

    It purges all emails and all information about the campaign.
    """

    full_queue = Router.FULL_QUEUE
    messages = list()

    campaign_name_ = campaign_name(cid)
    lang = campaign_language(cid)
    emails_in_campaign = set()
    attribution_for_email = dict()
    ( gm_email, full_gm, gm_attribution ) = campaign_gm(cid)
    emails_in_campaign.add( gm_email )
    campaign_characters = all_characters(cid)

    for character in campaign_characters:
        if not int(character['is_npc']):
            emails_in_campaign.add(character['controller'])

    for email in emails_in_campaign:
        attribution_for_email[email] = get_attribution(email)

    seen_ids = set()
    for key in full_queue.keys():
        msg = full_queue.get(key)
        if msg is None:
            continue
        msg_id = get_message_id(msg)
        if msg_id in seen_ids:
            continue
        seen_ids.add(msg_id)

        name, sender = parseaddr(msg['from'])
        if sender in emails_in_campaign:
            msg_epoch = mktime_tz(parsedate_tz(msg['Date']))
            messages.append( { 'epoch' : msg_epoch, 'msg' : msg, 'key' : key } )

    # sort messages by date
    messages = sorted(messages, key=lambda t: t['epoch'])

    # create nonce
    while True:
        nonce = hashlib.sha256("%s-%d" %
                                   (cid, random.randint(0,9001))).hexdigest()[0:10]
        target_zip = "%s/%s.zip" % ( campaigns_report_folder, nonce ) 
        if not os.path.exists(target_zip):
            break
    tmp_folder = "/tmp/" + nonce
    os.mkdir(tmp_folder)

    # First pass, compute statistics
    gm_emails = 0
    gm_emails_as_npcs = 0
    pc_emails = 0
    dice_rolls = 0

    for t in messages:
        msg = t['msg']

        name, sender = parseaddr(msg['From'])
        recepients = get_recipients(msg)
        is_dice = False
        rcpts = list()
        if 'pm-dice' in sender or 'pm-roll' in sender:
            is_dice = True
        else:
            for rcpt in recepients:
                if 'pm-dice' in rcpt or 'pm-roll' in rcpt:
                    is_dice = True
                elif not rcpt.startswith('as-'):
                    rcpts.append(rcpt)
        if is_dice:
            dice_rolls += 1
            t['flags'] = { 'dice' : True }
        else:
            if sender == gm_email:
                gm_emails += 1
                t['flags'] = { 'gm' : True }
                for rcpt in recepients:
                    if rcpt.startswith('as-'):
                        gm_emails_as_npcs += 1
                        t['flags']['as'] = rcpt[3:]
            else:
                pc_emails += 1
                placed = place_sender(msg)
                if len(placed) == 3:
                    short_form = placed[2]
                    t['flags'] = { 'pc' : short_form }
                else:
                    t['flags'] = 'UNKNOWN'
        t['recipients'] = rcpts
        
    #### front matter
    tex = codecs.open(tmp_folder + "/campaign.tex", 'w', 'utf-8')
    md = codecs.open(tmp_folder + "/campaign.md", 'w', 'utf-8')

    tex.write(view.render(locals(), "%s/campaign.tex" % (lang,)))
    # GM, PC players, NPC players, attributions, licence
    
    all_mails = len(messages)
    print_characters = list()
    for character in campaign_characters:
        print_characters.append({ 'type' : ("NPC" if int(character['is_npc']) else "PC"),
            'full_name': character['name'], 'short_form': character['address'],
            'attribution' : (character['alt_attribution'] if 'alt_attribution' in character else attribution_for_email[character['controller']]) })
    # TODO start date, end date
    md.write(view.render(locals(), "%s/campaign.md" % (lang,)))

    for t in messages:
        msg = t['msg']

        # header (includes who send it, potentially as-XYZ and to/cc)
        rcpts = ", ".join(t['recipients'])
        if 'dice' in t['flags']:
            md.write(view.render(locals(), "%s/dice_roll.md" % (lang,)))
            md.write(u"---------\n")
        elif 'gm' in t['flags']:
            if 'as' in t['flags']:
                md.write(u"%s (GM) → %s\n" % (t['flags']['as'], rcpts))
                md.write(u'------------------------\n')
            else:
                md.write(u"GM → %s\n" % (rcpts,))
                md.write(u'------------------------\n')                
        else:
            md.write(u"%s (PC) → %s\n" % (t['flags']['pc'] , rcpts))
            md.write(u'------------------------\n')

        md.write(t['key'] + "\n\n")
        if msg['subject']:
            md.write(u"Subject: %s\n\n" % (msg['subject'],))
        
        # content
        full_content = sanitize(msg.body())
        md.write(full_content)
        md.write("\n")

        #TODO typeset email

    md.close()
    tex.close()

    # render to PDF
    if os.path.exists("/usr/bin/pdflatex") and os.path.exists("/usr/bin/pandoc"):
        call("cd %s; /usr/bin/pandoc campaign.md -o messages.tex" % (tmp_folder,), shell=True)
        call("cd %s; pdflatex campaign.tex; pdflatex campaign.tex; pdflatex campaign.tex" % (tmp_folder,), shell=True)

    # render to HTML
    if os.path.exists("/usr/bin/pandoc"):
        call("cd %s; /usr/bin/pandoc campaign.md -o campaign.html" % (tmp_folder,), shell=True)

    # zip source texts + PDF to target_zip
    call("cd /tmp; /usr/bin/zip -r %s %s" % (os.path.realpath(target_zip), nonce), shell=True)

    if purge:
        # delete messages from full queue
        for t in messages:
            full_queue.remove(t['key'])

        # purge campaign from redis
        delete_campaign(cid)

    return nonce
