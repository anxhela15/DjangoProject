# Generated by Django 2.0.1 on 2018-09-12 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0100_remove_file_deployer'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='deployer',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
