# Generated by Django 2.0.1 on 2018-08-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_file_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='subject',
            field=models.CharField(default='DEFAULT', max_length=30),
        ),
    ]
