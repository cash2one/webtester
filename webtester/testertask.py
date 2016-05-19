from __future__ import absolute_import
from __future__ import print_function
import json
from celery import shared_task
from .casetester import CaseTester


@shared_task
def test_testpost(test_post):
    cases_json = json.loads(test_post)
    cases = cases_json['caseList']
    tester = CaseTester()
    for case in cases:
        tester.set_case_json(case)
        tester.do_test()


@shared_task
def test_post(tetpost):
    return tetpost + ' world'
