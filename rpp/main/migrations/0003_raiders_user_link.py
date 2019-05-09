# Generated by Django 2.1 on 2019-03-29 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20190327_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='raiders',
            name='user_link',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='link', to=settings.AUTH_USER_MODEL, verbose_name='user_link'),
        ),
    ]
