# Generated by Django 4.1 on 2022-08-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=200)),
                ('watt', models.IntegerField()),
            ],
            options={
                'db_table': 'index',
            },
        ),
    ]
