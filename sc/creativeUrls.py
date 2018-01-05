# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.creative, name="creative"),
    url(r'^design/$', views.design, name="design"),
    url(r'^conception/$', views.conception, name="conception"),
    url(r'^story/$', views.story, name="story"),
    url(r'^invention/$', views.invention, name="invention"),
    url(r'^music/$', views.music, name="music"),
    url(r'^video/$', views.video, name="video"),
    url(r'^new/$', views.newCreative, name="creative"),
    url(r'^new/design/$', views.newDesign, name="design"),
    url(r'^new/conception/$', views.newConception, name="conception"),
    url(r'^new/story/$', views.newStory, name="story"),
    url(r'^new/invention/$', views.newInvention, name="invention"),
    url(r'^new/music/$', views.newMusic, name="music"),
    url(r'^new/video/$', views.newVideo, name="video"),

]

