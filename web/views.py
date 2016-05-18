from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import JsonResponse
from webtester.testertask import test_testpost
from webtester.testertask import test_post as test_post_print
from celery import Celery
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    template = loader.get_template('web/index.html')
    return HttpResponse(template.render())


def login_view(request):
    next_page = request.GET['next']
    if next_page is None:
        next_page = '/index'
        # show login page
    c = {'next': next_page}
    c.update(csrf(request))
    if request.method == 'GET':
        c['error_msg'] = ''
        return render_to_response('web/login.html', c)
    elif request.method == 'POST':
        # login api
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.GET['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_page)
                # Redirect to a success page.
            else:
                c['error_msg'] = {'error_msg', 'disabled account'}
                return render_to_response('web/login.html', c)
        else:
            c['error_msg'] = 'account or password error'
            return render_to_response('web/login.html', c)


@login_required(login_url='/login')
def dashboard(request):
    template = loader.get_template('web/dashboard.html')
    return HttpResponse(template.render())


@csrf_exempt
def add_test_post(request):
    test_post = request.POST['test_post']
    test_post_print.delay(test_post)
    if request.method == 'GET':
        return JsonResponse({'errno': 3, 'msg': 'only support post'})
    if request.user.is_authenticated():
        test_post = request.POST['test_post']
        if test_post is None:
            return JsonResponse({'errno': 2, 'msg': 'test_post needed'})
        test_post_print.delay(test_post)
        return JsonResponse({'errno': 0, 'msg': 'test_post add to queue success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'this api need to be authed'})
