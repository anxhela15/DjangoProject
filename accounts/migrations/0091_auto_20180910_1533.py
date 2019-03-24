# Generated by Django 2.0.1 on 2018-09-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0090_task_progress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='progress',
            new_name='finished_todos',
        ),
        migrations.AddField(
            model_name='task',
            name='to_dos',
            field=models.IntegerField(default=0),
        ),
    ]
