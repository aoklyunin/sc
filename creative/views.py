from sc.models import Submission
from sc.views import getCreativeByType


def creative(request):
    return getCreativeByType(request, '',Submission.TP_CREATIVE)


def design(request):
    return getCreativeByType(request,  'Дизайн',Submission.TP_CREATIVE)


def conception(request):
    return getCreativeByType(request, 'Концепция',Submission.TP_CREATIVE)


def story(request):
    return getCreativeByType(request,  'Сюжет',Submission.TP_CREATIVE)


def invention(request):
    return getCreativeByType(request,  'Изобретения',Submission.TP_CREATIVE)


def music(request):
    return getCreativeByType(request, 'Музыка',Submission.TP_CREATIVE)


def video(request):
    return getCreativeByType(request, 'Видео',Submission.TP_CREATIVE)

