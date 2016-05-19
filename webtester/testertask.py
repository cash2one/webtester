from __future__ import absolute_import
from __future__ import print_function
import json
from celery import shared_task
from .casetester import CaseTester
import urllib, urllib2
import json
from webtester.settings import ADD_REPORT_LIST_API
import traceback


@shared_task
def test_testpost(test_post):
    cases_json = json.loads(test_post)
    cases = cases_json['caseList']
    tester = CaseTester()
    for case in cases:
        tester.set_case_json(case)
        report_list = tester.do_test()
        data = {'report_list': json.dumps(report_list)}
        data = urllib.urlencode(data)
        try:
            request = urllib2.Request(ADD_REPORT_LIST_API, data)
            res = urllib2.urlopen(request)
            print(res)
        except:
            traceback.print_exc()


@shared_task
def test_post(tetpost):
    return tetpost + ' world'
