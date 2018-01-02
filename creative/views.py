from sc.models import Submission
from sc.views import getCreativeByType


def creative(request):
    return getCreativeByType(request,  'creative_lists/creative.html', '',Submission.TP_CREATIVE)


def design(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Дизайн',Submission.TP_CREATIVE)


def conception(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Концепция',Submission.TP_CREATIVE)


def story(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Сюжет',Submission.TP_CREATIVE)


def invention(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Изобретения',Submission.TP_CREATIVE)


def music(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Музыка',Submission.TP_CREATIVE)


def video(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Видео',Submission.TP_CREATIVE)

