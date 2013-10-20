from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    response = render_to_response('poissonmagique/index.html', dict(), RequestContext(request))
    return response

