# Generated by Django 2.0.7 on 2018-11-12 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180811_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='social_app',
            field=models.CharField(blank=True, choices=[('FB', 'Facebook'), ('IG', 'Instagram'), ('YT', 'Youtube'), ('TW', 'Twitter')], default=None, max_length=2),
        ),
    ]