from config.settings import server_name_config, campaigns_report_folder
from email.utils import parseaddr, formataddr, getaddresses, parsedate_tz, mktime_tz
from salmon.routing import Router
import table as t
import logging
import re
import os
import hashlib
import random
import codecs
from subprocess import call
from campaign import all_characters, campaign_gm, get_character, campaign_language, campaign_name, get_recipients

def end_campaign(cid, purge=True):
    """Ends a campaign, returns the list of email addresses to email,
    plus the code for downloading the log.

    It purges all emails and all information about the campaign.
    """

    full_queue = Router.FULL_QUEUE
    messages = list()

    name = campaign_name(cid)
    lang = campaign_lang(cid)
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

    for key in full_queue.keys():
        msg = full_queue.get(key)

        name, sender = parseadd(msg['from'])
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
    tmp_folder = "/tmp/" % (nonce,)
    os.mkdir(tmp_folder)

    # First pass, compute statistics
    gm_email_as_npcs = 0
    gm_emails = 0
    pc_emails = 0
    dice_rolls = 0

    for t in messages:
        msg = t['msg']

        name, sender = parseaddr(msg['From'])
        recepients = get_recipients(msg)
        is_dice = False;
        if 'pm-dice' in sender or 'pm-roll' in sender:
            is_dice = True
        else:
            for rcpt in recepients:
                if 'pm-dice' in rcpt or 'pm-roll' in rcpt:
                    is_dice = True
        if is_dice:
            dice_rolls += 1
            t['flags'] = { 'dice' : True }
        else:
            if sender == gm_email:
                gm_emails += 1
                t['flags'] = { 'gm' : True }
                for rcpt in recepients:
                    if rcpt.startswith('as-'):
                        gm_email_as_npcs += 1
                        t['flags']['as'] = rcpt[3:]
            else:
                pc_emails += 1
                placed = c.place_sender(msg)
                if len(placed) == 2:
                    short_form = placed[2]
                    t['flags'] = { 'pc' : short_form }
        
    #### front matter
    tex = codecs.open(tmp_folder + "/campaign.tex", 'w', 'utf-8')
    md = codecs.open(tmp_folder + "/campaign.md", 'w', 'utf-8')

    tex_lang = "english"
    if lang == "es":
        tex_lang = "spanish"

    tex.write(u"""
\documentclass[
oneside,
openright,
titlepage,
dottedtoc,
numbers=noenddot,
headinclude,
footinclude=true,
cleardoublepage=empty,
abstractoff,
paper=letter,
fontsize=11pt,
american
]
{scrreprt}
\PassOptionsToPackage{utf8}{inputenc}
\usepackage{inputenc}
\usepackage[%s]{babel}
\usepackage[pdfspacing]{classicthesis}

\parskip 1.5ex

\begin{document}
\selectlanguage{%s}

""" % (tex_lang,tex_lang))
    if lang == "en":
        tex.write(u"""\title{%s}
\subtitle{Poisson Magique Campaign Report}
""" ^% (name,)) 
    elif lang == "es":
        tex.write(u"""\title{%s}
\subtitle{Reporte de Juego en Poisson Magique}
""" % (name,))
        
    tex.write(u"""\maketitle
""")

    # GM, PC players, NPC players, attributions, licence
    
    md.write(u"Poisson Magique Campaign: %s\n" % (name,))
    md.write(u"===========================================\n\n\n")
    md.write(u"Attributions\n")
    md.write(u"------------\n\n")
    md.write(u"GM: %s\n" % gm_attribution)
    for character in campaign_characters:
        md.write(u'%s %s (%s): %s\n' % ("NPC" if int(character('is_npc')) else "PC",
            character['fullname'], character['address'],
            character['alt_attribution'] if 'alt_attribution' in character else attribution_for_email[character['controller']]))

    md.write(u"\nAll content under license CC-BY-SA\n\n")

    # total number of emails sent
    md.write(u"Numbers\n")
    md.write(u"-------\n\n")
    md.write(u"""Number of emails received: %d
GM emails: %d (as NPCs %d)
PC emails: %d
Dice roll emails: %d
""" % (len(messages), gm_emails, gm_emails_as_npcs, pc_emails, dice_rolls))

    # TODO start date, end date

    for t in messages:
        msg = t['msg']


        # header (includes who send it, potentially as-XYZ and to/cc)
        if 'dice' in t['flags']:
            md.write("Dice Roll\n")
            md.write("---------\n")
        elif 'gm' in t['flags']:
            if 'as' in t['flags']:
                md.write(t['flags']['as'] + u" (GM)\n")
                md.write('------------------------\n')
        else:
            md.write(t['flags']['pc'] + u" (PC)\n")
            md.write('------------------------\n')

        # content
        full_content = sanitize(msg.body())
        md.write(full_content)

        #TODO typeset email



    #TODO end matter

    # render to PDF
    md.close()
    tex.close()

    #call("cd %s; pdflatex campaign.tex; pdflatex campaign.tex; pdflatex campaign.tex" % (tmp_folder,), shell=True)

    # zip source texts + PDF to target_zip
    call("cd /tmp; zip -r %s %s" % (os.path.realpath(target_zip), nonce), shell=True)

    if purge:
        # delete messages from full queue
        for t in messages:
            full_queue.remove(t['key'])

        # purge campaign from redis
        delete_campaign(cid)

    return nonce
