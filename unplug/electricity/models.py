from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Entries(models.Model):
    uuid = models.CharField(max_length=200)
    watt = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = "index"

    def __str__(self):
        return f'[{self.uuid}]{self.created_at}'


class Metadata(models.Model):
    month = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(12)])
    average_Kwatt = models.IntegerField()

    class Meta:
        db_table = "metadata"

    def __str__(self):
        return f'{self.month}월 사용량'
