# Generated by Django 2.0.6 on 2018-07-03 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
