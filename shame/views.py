from django.shortcuts import render

# Create your views here.
def shame(request):
    return render(request, 'shame/main.html', {})

