# -*- coding: utf-8 -*-

import collections
import datetime
from hashlib import md5

import mistune
from django.contrib.auth.models import User
from django.db import models
from sc_main.settings.common import KARMA_RED_LIMIT, KARMA_RED_COLOR, KARMA_GREEN_LIMIT, KARMA_YELLOW_COLOR, \
    KARMA_GREEN_COLOR


class ScUser(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=35, null=True, default=None,
                                  blank=True)
    last_name = models.CharField(max_length=35, null=True, default=None,
                                 blank=True)
    date = models.DateField(null=True, default=None,
                            blank=True)

    email = models.EmailField(null=True, blank=True, default=None)
    about_text = models.TextField(blank=True, null=True, max_length=500,
                                  default=None)
    about_html = models.TextField(blank=True, null=True, default=None)
    gravatar_hash = models.CharField(max_length=32, null=True, blank=True,
                                     default=None)
    display_picture = models.NullBooleanField(default=False)
    homepage = models.URLField(null=True, blank=True, default=None)
    instagram = models.CharField(null=True, blank=True, max_length=39,
                                 default=None)
    twitter = models.CharField(null=True, blank=True, max_length=39,
                               default=None)
    fb = models.CharField(null=True, blank=True, max_length=39,
                          default=None)
    vk = models.CharField(null=True, blank=True, max_length=39,
                          default=None)
    telegram = models.CharField(null=True, blank=True, max_length=39,
                                default=None)

    youtube = models.CharField(null=True, blank=True, max_length=39,
                               default=None)

    creativeKarma = models.IntegerField(default=0)
    powerKarma = models.IntegerField(default=0)

    def getDate(self):
        if self.date == None:
            return ""
        return self.date.strftime("%d/%m/%y")

    def update_profile_data(self):
        self.about_html = mistune.markdown(self.about_text)
        if self.display_picture:
            self.gravatar_hash = md5(self.email.lower().encode('utf-8')).hexdigest()

    def __unicode__(self):
        return "<ScUser:{}>".format(self.user.username)

    def __str__(self):
        return "<ScUser:{}>".format(self.user.username)

    def getColorKarma(self, val):
        if val < KARMA_RED_LIMIT:
            return KARMA_RED_COLOR
        elif val < KARMA_GREEN_LIMIT:
            return KARMA_YELLOW_COLOR
        else:
            return KARMA_GREEN_COLOR

    def getCreativeKarmaColor(self):
        return self.getColorKarma(self.creativeKarma)

    def getPowerKarmaColor(self):
        return self.getColorKarma(self.powerKarma)

    def getShortCreativeKarma(self):
        return self.getShortKarmaVal(self.creativeKarma)

    def getShortPowerKarma(self):
        return self.getShortKarmaVal(self.powerKarma)

    def getShortKarmaVal(self, val):
        if val == 0:
            return "0"
        si = {1: "",
              1E3: "k",
              1E6: "M",
              1E9: "G"}
        for i in reversed(range(0, 9, 3)):
            curVal = 10 ** i
            if (abs(val) >= curVal):
                return str(int(val / curVal)) + si[curVal]
