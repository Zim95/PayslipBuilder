# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile Model to add profile 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    about = models.TextField(max_length=500, blank=True)
    profile_photo = models.FileField(upload_to="photo/", default=None)
    portfolio_site = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Education(models.Model):
    profile_id = models.ForeignKey(
        Profile,
        verbose_name=(""),
        on_delete=models.CASCADE
    )
    
    institute = models.CharField(max_length=500, null=False, blank=False)
    
    degree_choices = (
        ("B.Tech", "Bachelor Of Technology"),
        ("M.Tech", "Master Of Technology"),
        ("BBA", "Bachelor of Business Administration"),
        ("MBA", "Master Of Business Administration"),
        ("Class 10", "High School"),
        ("Class 12", "Higher Secondary School")
    )
    
    completion_year_choices = (
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019")
    )

    start_year_choices = (
        ("2013", "2013"),
        ("2014", "2014"),
        ("2015", "2015")
    )

    degree = models.CharField(max_length=20, choices=degree_choices, default="B.Tech")
    year_of_starting = models.CharField(
        max_length=20,
        choices=start_year_choices,
        default="2017"
    )
    year_of_completion = models.CharField(
        max_length=20,
        choices=completion_year_choices,
        default="2017"
    )

    def __str__(self):
        return self.institute


class SocialLinks(models.Model):
    profile_id = models.ForeignKey(
        Profile,
        verbose_name=(""),
        on_delete=models.CASCADE
    )
    sitename = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.sitename


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(models.FileField(upload_to="resume/", default=None))

    def __str__(self):
        return self.user.username