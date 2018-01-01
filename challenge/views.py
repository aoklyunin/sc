from django.shortcuts import render

# Create your views here.
from creative.views import getCreativeByType


def challenge(request):
    return getCreativeByType(request, 'public/creative_list.html', '', True)


def make(request):
    return render(request, 'challenge/make.html', {})

def take(request):
    return render(request, 'challenge/take.html', {})
