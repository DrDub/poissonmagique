from django.db import models

class CommandLog(models.Model):
    """
    Command log
    """
    issuer = models.ForeignKey(Human)
    when = models.DateTimeField()
    campaign = models.ForeignKey(Campaign, null=True, blank=True)
    command_json = models.TextField()

class Blocks(models.Model):
    """
    Blocked emails
    """
    address = models.EmailField()


