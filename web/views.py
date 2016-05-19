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
import time
import json
from web.models import *
from celery import Celery
from django.views.decorators.csrf import csrf_exempt
import urllib
import httplib
from webtester.settings import PAGE_CRAWLER_URL


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


@login_required(login_url='/login')
def report(request):
    template = loader.get_template('web/report.html')
    return HttpResponse(template.render())


@csrf_exempt
def add_test_post(request):
    if request.method == 'GET':
        return JsonResponse({'errno': 3, 'msg': 'only support post'})
    if request.user.is_authenticated():
        test_post_data = request.POST['test_post']
        if test_post_data is None:
            return JsonResponse({'errno': 2, 'msg': 'test_post needed'})
        test_post_data = __save_testpost(test_post_data, request)
        test_testpost.delay(test_post_data)
        return JsonResponse({'errno': 0, 'msg': 'test_post add to queue success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'this api need to be authed'})


@csrf_exempt
def add_post_report(request):
    pass


def crawler(request):
    url = request.GET['url']
    if url is None or url == '':
        return JsonResponse({'errno': 1, 'msg': 'need url'})
    params = urllib.urlencode({'url': url})
    f = urllib.urlopen("%s?%s" % (PAGE_CRAWLER_URL, params))
    page = f.read()
    return HttpResponse(page)


# @csrf_exempt
# def show_report(request):
#     if request.user.is_authenticated():
#         return JsonResponse({'errno': 0, 'msg': 'test_post add to queue success'})
#     else:
#         return JsonResponse({'errno': 1, 'msg': 'this api need to be authed'})


def __save_testpost(testpost, request):
    # save post
    test_post_json = json.loads(testpost, 'utf8')
    name = test_post_json.get('name', '%d:%s' % (request.user.id, str(time.time())))
    post = TestPost(user_id=request.user.id, name=name, ext=testpost,status=0)
    post.save()
    # save caseList
    test_post_json = json.loads(testpost, 'utf8')
    test_post_json['postId'] = post.id
    test_post_json['userId'] = request.user.id
    case_list = test_post_json['caseList']
    for i in range(0, len(case_list)):
        case = case_list[i]
        case_entry = Case(name=case.get('name', ''),
                          url=case.get('url', ''),
                          repeat_time=case.get('repeatTime', 1),
                          check_wait_time=case.get('checkWaitTime', 1),
                          browsers=case.get('browsers', '[firefox]'),
                          browser_window_size=case.get('browserWindowSize'),
                          screen_resolution=case.get('screenResolution'),
                          browser_scroll_position=case.get('browserScrollPosition'),
                          test_post=post,
                          ext=''
                          )
        case_entry.save()
        test_post_json['caseList'][i]['caseId'] = case_entry.id
        action_list = case.get('actionList')
        for action in action_list:
            action_entry = Action(xpath=action.get('xpath', ''),
                                  action_type=action.get('actionType'),
                                  input=action.get('input', ''),
                                  wait_time=action.get('waitTime', 0),
                                  case=case_entry,
                                  ext='')
            action_entry.save()

        check_list = case.get('checkList')
        for check in check_list:
            check_entry = Check(xpath=check.get('xpath', ''),
                                check_type=check.get('checkType'),
                                check_result=2,
                                ext='',
                                case=case_entry)
            check_entry.save()

    return json.dumps(test_post_json)
