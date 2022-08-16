from django.db import models
from datetime import datetime

class Entries(models.Model):
    uuid = models.CharField(max_length=200)
    watt = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now())
    class Meta:
        db_table="index"