from django.utils import timezone

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=256, null=False)
    email = models.CharField(max_length=256, unique=True, null=False)
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    friends = models.ManyToManyField('self')

    def str(self):
        return f'{self.username}계정'


class Device(models.Model):
    serial = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name="device")

    def str(self):
        return f'{self.user_id.username}의 device (: {self.serial[:6]}..)'
