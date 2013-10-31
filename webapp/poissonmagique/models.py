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

    def is_gm(self):
        campaign = self.campaign
        if campaign is None:
            return False
        return campaign.gm == self

class Campaign(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url = models.URLField(null=True, blank=True)
    # INVARIANT: is_active => \forall human in players \union { gm }: human.campaign == self
    gm = models.ForeignKey(Human, related_name='gm')
    # players does not include gm
    players = models.ManyToManyField(Human, related_name='players', default=None)
    #players = models.ForeignKey(Human, related_name='player')
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
    mail_address = models.EmailField(db_index=True)

    # TODO: mail_address is unique for a given campaign

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
    author_character = models.ForeignKey(Character, null=True)
    author_human = models.ForeignKey(Human)
    text = models.TextField()
    when = models.DateTimeField()

class FragmentRelation(models.Model):
    """
    A relation between two fragments / messages
    """
    source = models.ForeignKey(Fragment, related_name='source')
    target = models.ForeignKey(Fragment, related_name='target')
    rel_type = models.ForeignKey(FragmentRelType, related_name='type')

class FragmentRelType(models.Model):
    """
    A relation type between fragments
    """
    name = models.CharField(max_length=50, db_index=True, unique=True)
    description = models.CharField(max_length=1024, unique=False, null=True, blank=True)

class Queue(models.Model):
    """
    A MailDir
    """
    name = models.CharField(max_length=255, db_index=True, unique=True)
    maildir = models.CharField(max_length=1024, db_index=True, unique=True)

    def __unicode__(self):
        return u"Q@" + self.name

class MessageID(models.Model):
    """
    A message in a MailDir
    """
    # 255 should be enough see http://www.mail-archive.com/synalist-public@lists.sourceforge.net/msg02843.html
    message_id = models.CharField(max_length=255, db_index=True)
    key = models.CharField(max_length=255, db_index=True)
    queue = models.ForeignKey(Queue)

    def __unicode__(self):
        return u"<" + self.message_id + u">" + self.queue.__unicode__()

    class Meta:
        unique_together = ( 'message_id', 'key', 'queue' )


class Message(Fragment):
    """
    An actual email between humans in character
    """
    message_id = models.CharField(max_length=255, db_index=True, unique=True)
    receivers_character = models.ManyToManyField(Character, related_name='receiver')
    receivers_human = models.ManyToManyField(Human, related_name='receiver')
    parts = models.ManyToManyField(Fragment, related_name='part')

    def __unicode__(self):
        return u"<" + self.message_id + u">"
        
from account.signals import email_confirmed, user_signed_up

def create_human(user, form, **kwargs):
    human = Human.objects.filter(user=user)
    if len(human) > 0:
        return

    human = Human(name=user.username, mail_address=user.email, user=user)
    human.save()

user_signed_up.connect(create_human)
