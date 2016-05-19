# __author__ = 'min'
# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
from time import *
import traceback
import win32api
from random import Random


class CaseTester:
    def __init__(self):
        self.case_json = None

    # def __init__(self, case_json):
    #     self.case_json = case_json

    def __parse_case_file(self):
        self.case_id=self.case_json['caseId']
        self.user_id=self.case_json['userId']
        self.name = self.case_json['name']
        self.url = self.case_json['url']
        self.browsers = self.case_json.get('browsers', ['chrome'])
        self.action_list = self.case_json.get('actionList', [])
        self.check_list = self.case_json.get('checkList', [])
        self.browser_window_size = self.case_json.get('browserWindowSize', [{'width': 1366, 'high': 768}])
        self.browser_scroll_position = self.case_json.get('browserScrollPosition',
                                                          {"x": 0, "y": 0})
        self.screen_resolution = self.case_json.get('screenResolution', {'width': 1366, 'high': 768})
        self.boxLength = self.case_json.get('length')
        self.chars = self.case_json.get('chars')

    def __open_browser(self, browser):
        # open browser
        if browser == 'chrome':
            self.driver = webdriver.Chrome()
        elif browser == 'firefox':
            self.driver = webdriver.Firefox()
        elif browser == 'IE':
            self.driver = webdriver.Ie()
        else:
            self.driver = webdriver.Chrome()

    def __do_actions(self):
        for action in self.action_list:
            xpath = action['xpath']
            do = action['actionType']
            if do == 'input':
                text_input = action['input']
                element = self.driver.find_element_by_xpath(xpath)
                self.driver.execute_script('arguments[0].scrollIntoView()', element)
                element.send_keys(text_input)
            elif do == 'clear':
                element = self.driver.find_element_by_xpath(xpath)
                self.driver.execute_script('arguments[0].scrollIntoView()', element)
                element.clear()
            elif do == 'click':
                element = self.driver.find_element_by_xpath(xpath)
                self.driver.execute_script('arguments[0].scrollIntoView()', element)
                element.click()

            elif do == 'inputBox':
                num = self.boxLength
                chars = self.chars
                text = self.randomStr(num, chars)
                element = self.driver.find_element_by_xpath(xpath)
                self.driver.execute_script('arguments[0].scrollIntoView()', element)
                element.send_keys(text)

    def __do_check(self):
        result_content = ''
        for check_index in range(0, len(self.check_list)):
            check = self.check_list[check_index]
            check_type = check['checkType']
            if check_type == 'expectedUrl' or check_type == 'expectedText':
                result_content = '%s<p>%d %s: ' % (result_content, check_index, check_type)
                expected = check['checkData']
                if check_type == 'expectedUrl':
                    real = self.driver.current_url
                else:
                    xpath = check['xpath']
                    real = self.driver.find_element_by_xpath(xpath).text
                result_content += ' excepted ' + expected
                result_content += ' real ' + real
                if expected == real:
                    result_content += ' pass</p>'
                else:
                    return {'result': False, 'result_content': result_content}
            elif check_type == 'screenContrast':
                img_name = self.name+str(check_index)
                self.driver.get_screenshot_as_file(
                    "./reportImg/" + img_name + str(self.width) + "x" + str(
                        self.high) + "@1.jpg")
                window = self.browser_scroll_position
                x = window['x']
                y = window['y']
                js = "window.scrollTo(" + str(x) + "," + str(y) + ")"
                self.driver.execute_script(js)
                self.driver.get_screenshot_as_file(
                    "./reportImg/" + img_name + str(self.width) + "x" + str(
                        self.high) + "@2.jpg")
            # elif check_type == 'expectedText':
            #     xpath = check['xpath']
            #     current_text = self.driver.find_element_by_xpath(xpath).text
            #     expected_text = check['checkData']
            #     print('expectedText:\t' + expected_text)
            #     print('currentText:\t' + current_text)
            #     if expected_text == current_text:
            #         print('pass')
            #     else:
            #         print('fail')
            elif check_type == 'printScreen':
                img_name = self.name+check_index
                self.driver.get_screenshot_as_file(
                    "./reportImg/" + img_name + str(self.width) + "x" + str(
                        self.high) + ".jpg")
        return {'result':True, 'result_content': result_content}

    def set_case_json(self, case_json):
        self.case_json = case_json

    def do_test(self):
        report_array=[]
        self.__parse_case_file()
        resolution_width = self.screen_resolution['width']
        resolution_height = self.screen_resolution['high']
        self.__change_resolution(resolution_width, resolution_height)
        for browser in self.browsers:
            report = {'caseId': self.case_id, 'userId': self.user_id,
                      'screen_resolution': '%dx%d' % (resolution_width, resolution_height)}
            self.browser = browser
            report['browser']=browser
            self.__open_browser(browser)
            for wh in self.browser_window_size:
                report['browser_window_size']=wh
                report['name']=self.name
                self.high = wh['high']
                self.width = wh['width']
                try:
                    self.driver.set_window_size(self.width, self.high)
                    self.driver.get(self.url)
                    # do actions
                    self.__do_actions()
                    sleep(1)
                    # check
                    result_info=self.__do_check()
                    report.update(result_info)
                except:
                    print('fail on exception')
                    traceback.print_exc()
                    report.update({'result': False, 'result_content': traceback.format_exc()})
                    continue
                finally:
                    # self.driver.refresh()
                    self.driver.delete_all_cookies()
                    report_array.append(report)
            self.driver.quit()
        return report_array


    def randomStr(self, num, randomChars):
        str = ''
        # chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(randomChars) - 1
        random = Random()
        for i in range(num):
            str += randomChars[random.randint(0, length)]
        return str

    @staticmethod
    def __change_resolution(resolution_width, resolution_height):
        dm = win32api.EnumDisplaySettings(None, 0)
        dm.PelsHeight = resolution_height
        dm.PelsWidth = resolution_width
        dm.BitsPerPel = 32
        dm.DisplayFixedOutput = 0
        # 1 is stretched to fill the larger screen space .2 is centered in the larger screen space
        win32api.ChangeDisplaySettings(dm, 0)
