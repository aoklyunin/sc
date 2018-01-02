from django.shortcuts import render

# Create your views here.
from creative.views import getCreativeByType


def challenge(request):
    return getCreativeByType(request, 'creative_lists/power.html', '', True)



def design(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Дизайн',True)


def conception(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Концепция',True)


def story(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'История',True)


def invention(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Изобретения',True)


def music(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Музыка',True)


def video(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Видео',True)

