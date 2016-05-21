from __future__ import absolute_import
from __future__ import print_function
from celery import shared_task
from .casetester import CaseTester
import json
from webtester.settings import ADD_REPORT_LIST_API, NOTIFY_TESt_POST_STATUS_API
import traceback
from webtester.util import post_to_url


@shared_task
def test_testpost(test_post):
    cases_json = json.loads(test_post)
    cases = cases_json['caseList']
    tester = CaseTester()
    report_id_list = []
    post_to_url(NOTIFY_TESt_POST_STATUS_API, {'post_id': cases_json['postId'], 'status': 'Task Exec'})
    has_error = False
    log = ''
    for case in cases:
        tester.set_case_json(case)
        try:
            report_list = tester.do_test()
            data = {'report_list': json.dumps(report_list)}
            res = post_to_url(ADD_REPORT_LIST_API, data)
            report_id_list.append(json.loads(res))
        except:
            log += '\n' + traceback.extract_stack()
            traceback.print_exc()
            has_error = True
            continue
    if has_error:
        post_to_url(NOTIFY_TESt_POST_STATUS_API,
                    {'post_id': cases_json['postId'], 'status': 'Task Complate With Exception',
                     'log': log})
    else:
        post_to_url(NOTIFY_TESt_POST_STATUS_API, {'post_id': cases_json['postId'], 'status': 'Task Success'})
