from django.shortcuts import render


# Create your views here.

def creative(request):
    return render(request, 'creative/main.html', {})


def design(request):
    return render(request, 'creative/design.html', {})

def conception(request):
    return render(request, 'creative/conception.html', {})

def story(request):
    return render(request, 'creative/story.html', {})

def invention(request):
    return render(request, 'creative/invention.html', {})

def music(request):
    return render(request, 'creative/music.html', {})

def video(request):
    return render(request, 'creative/video.html', {})
