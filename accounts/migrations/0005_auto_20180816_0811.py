# Generated by Django 2.0.1 on 2018-08-16 08:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_userextend_no_deployments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserExtend',
            new_name='Profile',
        ),
    ]
