# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from api.models import Profile, Education, SocialLinks

admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(SocialLinks)