from django.db import models
from django.contrib.auth.models import User

class UserState(models.Model):
    """
    State for Lamson serialization
    """
    created_on = models.DateTimeField(auto_now_add=True)
    state_key = models.CharField(max_length=512)
    from_address = models.EmailField()
    state = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s:%s (%s)" % (self.state_key, self.from_address, self.state)

class Human(models.Model):
    """
    A person behind an email account. Users can have several humans associated with them.
    """
    name = models.CharField(max_length=200)
    mail_address = models.EmailField(db_index=True, unique=True)
    # each human can be associated only with one campaign at a given time
    campaign = models.ForeignKey('Campaign', null=True, blank=True)
    user = models.ForeignKey(User, null=True)
    is_bouncing = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name + u" <" + self.mail_address + u">"

class Campaign(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url = models.URLField(null=True, blank=True)
    # INVARIANT: is_active => \forall human in players \union { gm  }: human.campaign == self
    gm = models.ForeignKey(Human, related_name='gm')
    # players does not include gm
    players = models.ForeignKey(Human, related_name='player')
    is_active = models.BooleanField(default=True, db_index=True)
    language = models.CharField(max_length=2)

    # TODO: consistency that the players and gm are all distinct

    # TODO: pointer to state

    def __unicode__(self):
        if self.is_active:
            return self.name
        else:
            return u"-" + self.name + u"-"

class Character(models.Model):
    controller = models.ForeignKey(Human)
    campaign = models.ForeignKey(Campaign)
    
    name = models.CharField(max_length=200)
    mail_address = models.EmailField(db_index=True, unique=True)

    # TODO: much more to come...

    def is_npc(self):
        return self.controller == self.campaign.gm

    def __unicode__(self):
        base = self.name + u" (" + (u"NPC" if self.is_npc() else u"PC") + u")"
        if self.campaign.is_active:
            return base
        else:
            return u"-" + base + u"-"


class Fragment(models.Model):
    """
    Part of a message
    """

    author = models.ForeignKey(Character, related_name='sender', unique=True)
    text = models.TextField()
    when = models.DateTimeField()

    related = models.ManyToManyField('self')

class Message(Fragment):
    """
    An actual email between humans in character
    """

    receivers = models.ForeignKey(Character, related_name='receiver')

    parts = models.ManyToManyField(Fragment, related_name='part')

