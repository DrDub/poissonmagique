from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from poissonmagique.models import Human
from django.conf import settings
from django.contrib.auth.decorators import login_required
from lamson.routing import Router
from lamson import queue

@login_required
def msg(request, msg_id=None):
    human = Human.objects.filter(user=request.user)
    if msg_id is None or \
            human is None or \
            len(human) == 0 or \
            not human[0].is_gm():
        return redirect('home')

    # check whether we can read the message
    msg = "None found"
    full_queue = queue.Queue("/home/pm/dev/run/full")
    for key in full_queue.keys():
        this_msg = full_queue.get(key)
        if this_msg is not None and this_msg['Message-ID'][1:-1] == msg_id:
            msg = this_msg

    params = { 'SITE_NAME': settings.SITE_NAME,
               'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
               'msg': msg,
               'msg_id' : msg_id }

    return render_to_response('poissonmagique/msg.html', params, RequestContext(request))




@login_required
def msg_all(request):
    human = Human.objects.filter(user=request.user)
    if human is None or \
            len(human) == 0 or \
            not human[0].is_gm():
        return redirect('home')

    msgs = []
    full_queue = queue.Queue("/home/pm/dev/run/full")
    for key in full_queue.keys():
        msg = full_queue.get(key)
        if msg is not None:
            msg['message_id'] = msg['Message-ID'][1:-1]
            msgs.append(msg)

    params = { 'SITE_NAME': settings.SITE_NAME,
               'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
               'msgs': msgs }

    return render_to_response('poissonmagique/msg_list.html', params, RequestContext(request))

@login_required
def msg_new(request):
    pass

@login_required
def msg_pending(request):
    pass

