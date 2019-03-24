# Generated by Django 2.0.1 on 2018-08-25 08:58

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0040_file_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='content',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=tinymce.models.HTMLField(default='DEFAULT'),
        ),
    ]