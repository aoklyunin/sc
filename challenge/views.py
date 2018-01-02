from django.shortcuts import render

# Create your views here.
from sc.models import Submission
from sc.views import getCreativeByType


def challenge(request):
    return getCreativeByType(request, 'creative_lists/power.html', '', Submission.TP_CHALLENGE)



def design(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Дизайн',Submission.TP_CHALLENGE)


def conception(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Концепция',Submission.TP_CHALLENGE)


def story(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'История',Submission.TP_CHALLENGE)


def invention(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Изобретения',Submission.TP_CHALLENGE)


def music(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Музыка',Submission.TP_CHALLENGE)


def video(request):
    return getCreativeByType(request, 'creative_lists/power.html', 'Видео',Submission.TP_CHALLENGE)

