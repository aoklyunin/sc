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
]

