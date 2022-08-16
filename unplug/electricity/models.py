from django.db import models

# Create your models here.

class Entries(models.Model):
    uuid = models.CharField(max_length=200)
    watt = models.IntegerField()
    class Meta:
        db_table="index"