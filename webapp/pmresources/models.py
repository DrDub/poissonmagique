from django.db import models

class Resource(models.Model):
    """
    A resource file (e.g., PC sheet)
    """
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=10)
    note = models.TextField()
    campaign = models.ForeignKey(Campaign)
    author_human = models.ForeignKey(Human)
    on_disk = models.CharField(max_length=1024, db_index=True)
