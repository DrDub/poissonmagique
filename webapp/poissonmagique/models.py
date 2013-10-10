from django.db import models

class Human(models.Model):
    name = models.CharField(max_length=200)
    mail_address = models.EmailField(db_index=True, unique=True)

class Campaign(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url = models.URLField(null=True, blank=True)
    gm = models.ForeignKey(Human, related_name='gm')
    players = models.ForeignKey(Human, related_name='player')

    # TODO: consistency that the players and gm are all distinct

    # TODO: pointer to state

class Character(models.Model):
    controller = models.ForeignKey(Human)
    
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

