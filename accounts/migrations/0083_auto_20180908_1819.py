# Generated by Django 2.0.1 on 2018-09-08 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0082_profile_new_task_finished'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='new_task_finished',
            new_name='new_task',
        ),
    ]
