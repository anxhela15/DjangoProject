# Generated by Django 2.0.1 on 2018-08-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20180822_1149'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Heading',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.TextField(),
        ),
    ]
