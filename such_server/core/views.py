import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def login_user(request):
    contents = json.loads(request.read())
    email = contents.get('email')
    password = contents.get('password')
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

def logout_user(request):
    logout(request)
    if request.method == 'GET':
        return redirect('/')
    return HttpResponse(status=204)

@ensure_csrf_cookie
def the_app(request):
    context = {
        'year': now().year,
        'user': None
    }
    if request.user.is_authenticated():
        context['user'] = {
            'email': request.user.email,
        }

    return render(request, 'index.html', context)
