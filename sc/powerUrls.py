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
]

