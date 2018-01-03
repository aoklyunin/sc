from django.shortcuts import render

# Create your views here.
from sc.models import Submission
from sc.views import getCreativeByType


def faq(request):
    return getCreativeByType(request, '', Submission.TP_FAQ)


