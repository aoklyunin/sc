from django.shortcuts import render

# Create your views here.
from creative.views import getCreativeByType


def challenge(request):
    return getCreativeByType(request, 'public/power_creative_list.html', '', True)



def design(request):
    return getCreativeByType(request, 'public/power_creative_list.html', 'Дизайн',True)


def conception(request):
    return getCreativeByType(request, 'public/power_creative_list.html', 'Концепция',True)


def story(request):
    return getCreativeByType(request, 'public/power_creative_list.html', 'История',True)


def invention(request):
    return getCreativeByType(request, 'public/power_creative_list.html', 'Изобретения',True)


def music(request):
    return getCreativeByType(request, 'public/power_creative_list.html', 'Музыка',True)


def video(request):
    return getCreativeByType(request, 'public/power_creative_list.html', 'Видео',True)

