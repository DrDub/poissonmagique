from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode
from django.conf import settings
from django.core.urlresolvers import reverse

from random import randrange
from datetime import datetime

from config.settings import server_name_config
from webapp.poissonmagique.models import Human
from models import SecureDice, Roll

class DiceRollForm(forms.Form):

    def __init__(self, gm, *args, **kwargs):
        super(DiceRollForm, self).__init__(*args, **kwargs)
        self.fields['who'] = forms.ModelChoiceField(queryset=gm.campaign.players)
        
    repeats = forms.IntegerField(max_value=1000,min_value=1, initial=1)
    sides = forms.IntegerField(max_value=1000,min_value=1, initial=6)
    add = forms.IntegerField(max_value=1000,min_value=-20, initial=0)
    set_repeat = forms.IntegerField(max_value=20,min_value=1, initial=1)
    description = forms.CharField(max_length=400, initial='1D6')
    what = forms.CharField(max_length=1024)

#TODO: make a gm_required decorator
@login_required
def new_roll(request):
    """
    Create a new dice roll
    """
    # fetch human
    human = Human.objects.get(user=request.user)
    if not human.is_gm():
        # TODO: error page
        return HttpResponseRedirect('/')

    # get the PCs for the campaign
    campaign = human.campaign
    #pcs = [ ( str(player.id), unicode(player) ) for player in campaign.players.all() ]
        
    if request.method == 'POST':
        form = DiceRollForm(human, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # create URL and SecureDice backend
            query_str = 'dq=%d&ds=%d&dm=%d&dt=%d' % ( data['repeats'],
                                                      data['sides'],
                                                      data['add'],
                                                      data['set_repeat'] )
            secure_dice = SecureDice(query_str=query_str)
            secure_dice.save()
            
            # create roll
            while True:
                hashid = randrange(100000, 999999)
                roll = Roll(when=datetime.utcnow(),
                            game_time=human.campaign.game_time,
                            hashid=hashid,
                            campaign=human.campaign,
                            description=data['description'],
                            what=data['what'],
                            target=data['who'],
                            implementation_key=secure_dice.id
                            )
                try:
                    roll.save()
                except Roll.IntegrityError:
                    next # clash hashid
                break
            
            return HttpResponseRedirect('/dice/show/%d' % (hashid,) )
    else:
        form = DiceRollForm(human)

    return render(request, 'dice/new.html', {
        'SITE_NAME': settings.SITE_NAME,
        'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
        'form': form,
    })

def roll(request, do_roll=False, hashid=None):
    if hashid is None:
        return HttpResponseRedirect('/')
    roll = Roll.objects.get(hashid=hashid)
    
    if do_roll:
        query_str = SecureDice.objects.get(pk=roll.implementation_key).query_str
        url = 'http://www.rpglibrary.org/software/securedice/?%s&%s' % (
            query_str,        
            urlencode( { 'to' : roll.target.mail_address,
                         'cc' : 'roll-%d@%s' % ( roll.hashid, server_name_config ),
                         'sub' : '%s (%s)' % (roll.description, roll.what[:40]) }
                       )
            )
    else:
        url = "http://%s%s" % (settings.SITE_NAME, reverse('dice_roll', kwargs={ 'hashid' : hashid }))
    
    return render(request, 'dice/roll.html', {
        'description' : roll.description,
        'what':roll.what,
        'url': url,
        'is_roll': do_roll,
        'hashid':hashid,
        'SITE_NAME': settings.SITE_NAME,
        'THEME_ACCOUNT_ADMIN_URL': settings.THEME_ACCOUNT_ADMIN_URL,
        })
