# Generated by Django 2.0.1 on 2018-09-08 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0081_auto_20180908_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='new_task_finished',
            field=models.BooleanField(default=False),
        ),
    ]