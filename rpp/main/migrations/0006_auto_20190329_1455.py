# Generated by Django 2.1 on 2019-03-29 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190329_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='raider',
            name='twitter_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='raider',
            name='youtube_channel',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
