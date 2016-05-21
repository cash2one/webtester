from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect


def index_view(request):
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
def dashboard_view(request):
    template = loader.get_template('web/dashboard.html')
    return HttpResponse(template.render())


@login_required(login_url='/login')
def report_view(request):
    template = loader.get_template('web/report.html')
    return HttpResponse(template.render())


@login_required(login_url='/login')
def task_view(request):
    template = loader.get_template('web/task.html')
    return HttpResponse(template.render())
