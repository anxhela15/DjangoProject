# Generated by Django 2.0.1 on 2018-09-17 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0110_auto_20180917_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='subject',
            new_name='skills',
        ),
    ]
