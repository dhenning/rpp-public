# Generated by Django 2.1 on 2019-03-29 17:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_remove_raiders_user_link'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Raiders',
            new_name='Raider',
        ),
    ]
