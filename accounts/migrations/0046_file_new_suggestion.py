# Generated by Django 2.0.1 on 2018-08-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_project_new_suggestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='new_suggestion',
            field=models.BooleanField(default=False),
        ),
    ]
