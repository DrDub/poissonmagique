from django.db import models
from webapp.poissonmagique.models import Campaign, Human

class RollBackend(models.Model):
    """
    A dice roll backend
    """
    class Meta:
        abstract = True
    
class SecureDice(RollBackend):
    """
    A dice roll backend
    """
    query_str = models.CharField(max_length=200)

class Roll(models.Model):
    """
    A dice roll
    """    
    when = models.DateTimeField()
    game_time = models.CharField(max_length=200, null=True, blank=True, default="")
    campaign = models.ForeignKey(Campaign)
    target = models.ForeignKey(Human, blank=True, null=True)
    description = models.CharField(max_length=400, null=True, blank=True, default="") # 3D6 + 5
    what = models.CharField(max_length=1024, null=True, blank=True, default="") # SAN because you see smth
    # characteristic (future, SAN)
    hashid = models.PositiveIntegerField(unique=True, db_index=True)
    implementation_type = models.IntegerField(default=1)
    implementation_key = models.IntegerField()
    outcome = models.ForeignKey('RollOutcome', null=True, blank=True, default=None, related_name='outcome')

    def __unicode__(self):
        return u"%s for %s%s" % (self.description, self.target, "" if self.outcome is None else " *")
    

class RollOutcome(models.Model):
    """
    The outcome of a dice roll
    """
    roll = models.ForeignKey(Roll)
    outcome_text = models.TextField()
    # outcome_value = models.IntegerField(null=True, blank=True, default=0)
    #is_successful = models.BooleanField(null=True, blank=True, default=False)

    def __unicode__(self):
        return u"Outcome for %s by %s" % (self.roll.description, self.roll.target)

