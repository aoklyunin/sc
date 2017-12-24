from django.shortcuts import render

# Create your views here.


def challenge(request):
    return render(request, 'challenge/main.html', {})


def make(request):
    return render(request, 'challenge/make.html', {})

def take(request):
    return render(request, 'challenge/take.html', {})
