# Generated by Django 2.0.1 on 2018-09-03 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0066_auto_20180903_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployment',
            name='date',
        ),
    ]
