# Generated by Django 2.0.7 on 2019-10-11 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20181022_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
    ]
