# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.powerCreative, name="challenge"),
    url(r'^design/$', views.designP, name="design"),
    url(r'^conception/$', views.conceptionP, name="conception"),
    url(r'^story/$', views.storyP, name="story"),
    url(r'^invention/$', views.inventionP, name="invention"),
    url(r'^music/$', views.musicP, name="music"),
    url(r'^video/$', views.videoP, name="video"),
    url(r'^new/$', views.newPowerCreative, name="creative"),
    url(r'^new/design/$', views.newDesignP, name="design"),
    url(r'^new/conception/$', views.newConceptionP, name="conception"),
    url(r'^new/story/$', views.newStoryP, name="story"),
    url(r'^new/invention/$', views.newInventionP, name="invention"),
    url(r'^new/music/$', views.newMusicP, name="music"),
    url(r'^new/video/$', views.newVideoP, name="video"),
]

