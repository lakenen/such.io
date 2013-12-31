from django.shortcuts import render

def the_app(request):
    context = {}
    return render(request, 'index.html', context)
