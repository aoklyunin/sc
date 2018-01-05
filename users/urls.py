# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^signin/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/$', views.user_profile, name="user_profile"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/$', views.user_creative, name="user_creative"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/video/$', views.user_video, name="user_video"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/design/$', views.user_design, name="user_design"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/conception/$', views.user_conception, name="user_conception"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/story/$', views.user_story, name="user_story"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/music/$', views.user_music, name="user_music"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)/creative/invention/$', views.user_invention, name="user_invention"),
    url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),
]
