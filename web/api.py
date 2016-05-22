import time
import json
import traceback
import urllib
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from webtester.testertask import test_testpost
from web.models import *
from django.views.decorators.csrf import csrf_exempt
from webtester.settings import PAGE_CRAWLER_URL
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from webtester.util import get_from_url,post_to_url


@csrf_exempt
def add_test_post(request):
    if request.method == 'GET':
        return JsonResponse({'errno': 3, 'msg': 'only support post'})
    if request.user.is_authenticated():
        test_post_data = request.POST['test_post']
        if test_post_data is None:
            return JsonResponse({'errno': 2, 'msg': 'test_post needed'})
        test_post_data = __save_testpost(test_post_data, request)
        print(test_post_data)
        test_testpost.delay(test_post_data)
        return JsonResponse({'errno': 0, 'msg': 'test_post add to queue success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'this api need to be authed'})


@csrf_exempt
def add_post_report_list(request):
    if request.method == 'GET':
        return JsonResponse({'errno': 3, 'msg': 'only support post'})
    else:
        report_list = json.loads(request.POST['report_list'], 'utf8')
        print(request.POST['report_list'])
        report_id_list = []
        for report in report_list:
            report_entry = Report(user_id=report['user_id'],
                                  case_id=report['case_id'],
                                  post_id=report['post_id'],
                                  case_name=report['name'],
                                  browser=report['browser'],
                                  resolution=report['resolution'],
                                  result=report['result'],
                                  result_content=report['result_content'],
                                  ext='')
            report_entry.save()
            report_id_list.append(report_entry.id)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': json.dumps(report_id_list)})


@csrf_exempt
def show_post_report_html(request):
    post_id = request.GET.get('post_id')
    if post_id is None:
        return render(request, 'web/error.html', {'msg': 'need post_id', 'desc': ''})
    post_entry = get_object_or_404(TestPost, id=post_id)
    if post_entry is None:
        return render(request, 'web/error.html', {'msg': 'post not found whith id ' + str(post_id), 'desc': ''})
    status = post_entry.status
    report_list = Report.objects.filter(post_id=post_id)
    return render(request, 'web/report_tep.html',
                  {'post_id': post_id, 'name': post_entry.name, 'status': status, 'report_list': report_list})


@csrf_exempt
def notify_test_post_status(request):
    post_id = request.POST.get('post_id')
    status = request.POST.get('status')
    log = request.POST.get('log')
    if post_id is None or status is None:
        return JsonResponse({'errno': 3, 'msg': 'need post_id and status'})
    try:
        post_entry = TestPost.objects.get(id=post_id)
        post_entry.status = status
        if log is not None:
            post_entry.exec_log += log
        post_entry.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    except:
        return JsonResponse({'errno': 4, 'msg': 'post not found'})


@csrf_exempt
def show_report_list(request):
    user_id = request.user.id
    if user_id is None:
        return JsonResponse({'errno': 1, 'msg': 'this api need authed'})
    else:
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        order = request.GET.get('order ')
        search = request.GET.get('search')
        sort = request.GET.get('sort')
        if offset is None or limit is None:
            return JsonResponse({'errno': 3, 'msg': 'need offset and limit'})
        report_list = Report.objects.filter(user_id=user_id).order_by('-create_time')
        if order is not None:
            if sort == 'desc':
                order = '-' + order
            report_list = report_list.order_by(order)
        if search is not None and search != '':
            report_list = report_list.filter(case_name__icontains=search)
        report_list = list(report_list.values())
        report_list = json.dumps(report_list, cls=DjangoJSONEncoder)
        return HttpResponse(report_list)


@csrf_exempt
def show_post_list(request):
    user_id = request.user.id
    if user_id is None:
        return JsonResponse({'errno': 1, 'msg': 'this api need authed'})
    else:
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        order = request.GET.get('order ')
        search = request.GET.get('search')
        sort = request.GET.get('sort')
        if offset is None or limit is None:
            return JsonResponse({'errno': 3, 'msg': 'need offset and limit'})
        post_list = TestPost.objects.filter(user_id=user_id).order_by('-create_time')
        if order is not None:
            if sort == 'desc':
                order = '-' + order
            post_list = post_list.order_by(order)
        if search is not None and search != '':
            post_list = post_list.filter(case_name__icontains=search)
        post_list = list(post_list.values())
        post_list = json.dumps(post_list, cls=DjangoJSONEncoder)
        return HttpResponse(post_list)


@csrf_exempt
def crawler(request):
    url = request.POST['url']
    if url is None or url == '':
        return JsonResponse({'errno': 1, 'msg': 'need url'})
    try:
        page = post_to_url(PAGE_CRAWLER_URL, request.POST)
        return HttpResponse(page)
    except:
        return JsonResponse({'errno': 1, 'msg': 'get html from proxy error ' + traceback.format_exc()})


def __save_testpost(testpost, request):
    # save post
    test_post_json = json.loads(testpost, 'utf8')
    name = test_post_json.get('name', '%d:%s' % (request.user.id, str(time.time())))
    post = TestPost(user_id=request.user.id, name=name, ext=testpost, status=0)
    post.save()
    # save caseList
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
        test_post_json['caseList'][i]['userId'] = request.user.id
        test_post_json['caseList'][i]['postId'] = post.id
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
