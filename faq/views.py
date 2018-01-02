from django.shortcuts import render

# Create your views here.
from creative.views import getCreativeByType


def faq(request):
    return getCreativeByType(request, 'creative_lists/faq.html', '', False)


