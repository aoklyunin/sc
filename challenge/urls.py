from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.challenge, name="challenge"),
    url(r'^make/$', views.make, name="make"),
    url(r'^take/$', views.take, name="take"),
]

