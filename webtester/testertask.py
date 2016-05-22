from __future__ import absolute_import
from __future__ import print_function
from celery import shared_task
from .casetester import CaseTester
import json
from webtester.settings import ADD_REPORT_LIST_API
from webtester.settings import NOTIFY_TEST_POST_STATUS_API, WEB_MASTER_PORT, WEB_MATER_HOST
import traceback
from webtester.util import post_to_url
from celery.utils.log import get_task_logger


@shared_task
def test_testpost(test_post):
    logger = get_task_logger(__name__)
    cases_json = json.loads(test_post)
    logger.info('test receive ' + test_post)
    cases = cases_json['caseList']
    tester = CaseTester()
    report_id_list = []
    post_to_url('http://%s:%d%s' % (WEB_MATER_HOST, WEB_MASTER_PORT, NOTIFY_TEST_POST_STATUS_API),
                {'post_id': cases_json['postId'], 'status': 'Task Exec'})
    has_error = False
    log = ''
    for case in cases:
        tester.set_case_json(case)
        try:
            report_list = tester.do_test()
            data = {'report_list': json.dumps(report_list)}
            res = post_to_url('http://%s:%d%s' % (WEB_MATER_HOST, WEB_MASTER_PORT, ADD_REPORT_LIST_API), data)
            report_id_list.append(json.loads(res))
        except:
            log += '\n' + traceback.format_exc()
            traceback.print_exc()
            has_error = True
            continue
    try:
        if has_error:
            logger.info('test complate with exception \n' + test_post + ' \n' + log)
            re = post_to_url('http://%s:%d%s' % (WEB_MATER_HOST, WEB_MASTER_PORT, NOTIFY_TEST_POST_STATUS_API),
                             {'post_id': cases_json['postId'], 'status': 'Task Complate With Exception',
                              'log': log})
            logger.debug('notify task re:' + re)
        else:
            logger.info('test success \n' + str(cases_json['postId']))
            re = post_to_url('http://%s:%d%s' % (WEB_MATER_HOST, WEB_MASTER_PORT, NOTIFY_TEST_POST_STATUS_API),
                             {'post_id': cases_json['postId'], 'status': 'Task Success'})
            logger.debug('notify task re:' + re)
    except:
        traceback.print_exc()
        logger.info('notify task post exception')
