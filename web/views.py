from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect

# Create your views here.

def index(request):
    template = loader.get_template('web/index.html')
    return HttpResponse(template.render())


def login_view(request):
    next_page = request.GET['next']
    if next_page == None:
        next_page = '/index'
        # show login page
    c = {'next': next_page}
    c.update(csrf(request))
    if request.method == 'GET':
        c['error_msg'] =''
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
                c['error_msg'] ={'error_msg', 'disabled account'}
                return render_to_response('web/login.html', c)
        else:
            c['error_msg']='account or password error'
            return render_to_response('web/login.html', c)


@login_required(login_url='/login')
def dashboard(request):
    template = loader.get_template('web/dashboard.html')
    return HttpResponse(template.render())


def test(request):
    template = loader.get_template('web/test.html')
    return HttpResponse(template.render())
