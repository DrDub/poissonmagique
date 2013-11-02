from django.db import models
from django.contrib.auth.models import User
import bitfield

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
        return u"%s <%s> (poisson-%d)" % (self.name, self.mail_address,  self.user.id)

    def is_gm(self, campaign=None):
        """
        Whether this human is a GM in the campaigh s/he is playing or in a given campaign
        """
        if campaign is None:
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
    campaign = models.ForeignKey(Campaign)
    text = models.TextField()
    when = models.DateTimeField()
    game_time = models.CharField(max_length=200, null=True)

class FragmentRelation(models.Model):
    """
    A relation between two fragments / messages
    """

    REL_TYPES = (
        ('FWD', 'Forward'),
        ('RPL', 'Reply'),
        ('REL', 'Related'),
    )
    source = models.ForeignKey(Fragment, related_name='source')
    target = models.ForeignKey(Fragment, related_name='target')
    rel_type = models.CharField(max_length=3, choices=REL_TYPES)

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
    subject = models.CharField(max_length=255, blank=True, null=True, default="")
    receivers_character = models.ManyToManyField(Character, related_name='receiver_character')
    receivers_human = models.ManyToManyField(Human, related_name='receiver_human')
    parts = models.ManyToManyField(Fragment, related_name='part')
    status = bitfield.BitField(flags=(
        ('read','Read'),
        ('deleted','Deleted'),
        ('private','Private')), default=0)

    def __unicode__(self):
        return u"%s: '%s' <%s>" % (unicode(self.when), self.subject, self.message_id)
        
from account.signals import email_confirmed, user_signed_up

def create_human(user, form, **kwargs):
    human = Human.objects.filter(user=user)
    if len(human) > 0:
        return

    human = Human(name=user.username, mail_address=user.email, user=user)
    human.save()

user_signed_up.connect(create_human)
