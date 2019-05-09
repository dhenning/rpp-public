from django.db import models
from django.contrib.auth.models import User


class Raider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_user = models.CharField(max_length=200, null=True, blank=True)
    birthday = models.DateField('birthday', null=True, blank=True)
    profile_pic = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    bio = models.TextField('bio', null=True, blank=True)
    twitch_name = models.CharField(max_length=200, null=True, blank=True)
    twitter_name = models.CharField(max_length=200, null=True, blank=True)
    youtube_channel = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, default="-------")

    objects = models.Manager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Raiders"


class Effect(models.Model):
    clip_id = models.CharField(max_length=200, default="None")
    name = models.CharField(max_length=200, default="None")
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Effects"
