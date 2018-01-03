from django.shortcuts import render

# Create your views here.
from sc.models import Submission
from sc.views import getCreativeByType


def challenge(request):
    return getCreativeByType(request, '', Submission.TP_CHALLENGE)



def design(request):
    return getCreativeByType(request, 'Дизайн',Submission.TP_CHALLENGE)


def conception(request):
    return getCreativeByType(request, 'Концепция',Submission.TP_CHALLENGE)


def story(request):
    return getCreativeByType(request,  'Сюжет',Submission.TP_CHALLENGE)


def invention(request):
    return getCreativeByType(request,  'Изобретения',Submission.TP_CHALLENGE)


def music(request):
    return getCreativeByType(request,  'Музыка',Submission.TP_CHALLENGE)


def video(request):
    return getCreativeByType(request, 'Видео',Submission.TP_CHALLENGE)

