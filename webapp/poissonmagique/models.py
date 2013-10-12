from django.db import models

class UserState(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    state_key = models.CharField(max_length=512)
    from_address = models.EmailField()
    state = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s:%s (%s)" % (self.state_key, self.from_address, self.state)

class Human(models.Model):
    name = models.CharField(max_length=200)
    mail_address = models.EmailField(db_index=True, unique=True)
    campaign = models.ForeignKey(Campaign, null=True)

class Campaign(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url = models.URLField(null=True, blank=True)
    gm = models.ForeignKey(Human, related_name='gm')
    players = models.ForeignKey(Human, related_name='player')

    # TODO: consistency that the players and gm are all distinct

    # TODO: pointer to state

class Character(models.Model):
    controller = models.ForeignKey(Human)
    
    name = models.CharField(max_length=200)
    mail_address = models.EmailField(db_index=True, unique=True)
    # TODO: much more to come...

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

