# Generated by Django 2.0.1 on 2018-08-23 21:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20180823_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dateofcreation',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 23, 21, 49, 49, 125136, tzinfo=utc)),
        ),
    ]
