# Generated by Django 2.0.1 on 2018-09-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0070_task_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='newtask',
            field=models.BooleanField(default=False),
        ),
    ]
