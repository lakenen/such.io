import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render


def login_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

            data = {
                'email': user.email,
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

    data = {
        'error': 'invalid email/password',
    }
    return HttpResponse(json.dumps(data), content_type='application/json', status=401)


def the_app(request):
    context = {}
    return render(request, 'index.html', context)
