from django.shortcuts import render_to_response
from django.template import RequestContext
from poissonmagique.models import Human
from django.conf import settings


def home(request):
    params = { 'SITE_NAME': settings.SITE_NAME,
               'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL }
    if request.user.is_authenticated():
        human = Human.objects.filter(user=request.user)
        if human is None or len(human) == 0:
            response = render_to_response('poissonmagique/index.html', params, RequestContext(request))
        else:
            if human[0].is_gm():
                response = render_to_response('poissonmagique/gm.html', params, RequestContext(request))
            else:
                response = render_to_response('poissonmagique/user.html', params, RequestContext(request))
    else:
        response = render_to_response('poissonmagique/index.html', params, RequestContext(request))

    return response

