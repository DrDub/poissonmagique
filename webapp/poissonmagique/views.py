from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from webapp.poissonmagique.models import Human
from django.conf import settings
from django.contrib.auth.decorators import login_required
from salmon.routing import Router
from salmon import queue
from queue_utils import sanity_check
from models import MessageID, Campaign


@login_required
def msg(request, msg_id=None):
    # TODO: change this from full log to campaign log
    human = Human.objects.filter(user=request.user)
    if msg_id is None or \
            human is None or \
            len(human) == 0 or \
            not human[0].is_gm():
        return redirect('home')

    # check whether we can read the message
    msg = "None found"
    full_queue = settings.QUEUE_FULL_LOG
    sanity_check(full_queue)
    try:
        message_id = MessageID.objects.get(message_id=msg_id,queue__maildir=full_queue.dir)
        key = message_id.key
        this_msg = full_queue.get(key)
        if this_msg is not None and this_msg['Message-ID'][1:-1] == msg_id:
            msg = this_msg
    except MessageID.DoesNotExist:
        pass

    params = { 'SITE_NAME': settings.SITE_NAME,
               'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
               'msg': msg,
               'msg_id' : msg_id }

    return render_to_response('poissonmagique/msg.html', params, RequestContext(request))

@login_required
def msg_list(request, filter=False):
    if request.user.is_staff:
        return _msg_all_admin(request)
    
    human = Human.objects.filter(user=request.user)
    if human is None or \
           len(human) == 0:
        return redirect('home')

    human = human[0]
    if 'campaign' in request.session:
        campaign = Campaign.objects.get(pk=int(request.session['campaign']))
    else:
        campaign = human.campaign
    
    if not human.is_gm(campaign):
        # TODO: PC message page
        return redirect('home')

    query = Message.objects.filter(campaign=campaign)
    if filter:
        query = query.filter(status=~Message.status.read)

    params = { 'SITE_NAME': settings.SITE_NAME,
               'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
               'msgs': query,
               'filter': filter,
             }

    return render_to_response('poissonmagique/msg_list.html', params, RequestContext(request))
                                        

def _msg_all_admin(request):
    msgs = []
    full_queue = settings.QUEUE_FULL_LOG
    for key in full_queue.keys():
        msg = full_queue.get(key)
        if msg is not None:
            msg['message_id'] = msg['Message-ID'][1:-1]
            msgs.append(msg)

    params = { 'SITE_NAME': settings.SITE_NAME,
               'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
               'msgs': msgs }

    return render_to_response('poissonmagique/msg_full_list.html', params, RequestContext(request))

@login_required
def msg_new(request):
    pass

