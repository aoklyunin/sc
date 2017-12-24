"""repo_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import debug_toolbar
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from sc.views import ehandler404, ehandler500

urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    # url(r'^users/', include('users.urls')),
    url(r'^', include("sc.urls")),
    url(r'^', include("users.urls")),
    url(r'^creative/', include("creative.urls")),
    url(r'^challenge/', include("challenge.urls")),
    url(r'^shame/', include("shame.urls")),
]

handler404 = ehandler404
handler500 = ehandler500

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
