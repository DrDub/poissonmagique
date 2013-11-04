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
    implementation = models.GenericForeignKey(RollBackend)
    outcome = models.ForeignKey('RollOutcome', null=True, blank=True, default=None, related_name='outcome')
    

class RollOutcome(models.Model):
    """
    The outcome of a dice roll
    """
    roll = models.ForeignKey(Roll)
    outcome_text = models.CharField(max_length=1024)
    # outcome_value = models.IntegerField(null=True, blank=True, default=0)
    #is_successful = models.BooleanField(null=True, blank=True, default=False)

