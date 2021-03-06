# Generated by Django 2.0.1 on 2018-08-19 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0016_remove_project_deployment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployment',
            name='deployer',
        ),
        migrations.AddField(
            model_name='project',
            name='deployer',
            field=models.ForeignKey(default=0, limit_choices_to={'groups__name': 'Deployers'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
