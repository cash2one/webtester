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
        self.report = None;

    # def __init__(self, case_json):
    #     self.case_json = case_json

    def __parse_case_file(self):
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
        for check in self.check_list:
            check_type = check['checkType']
            if check_type == 'expectedUrl':
                expected_url = check['checkData']
                real_url = self.driver.current_url
                print('expectedUrl:\t' + expected_url)
                print('currentUrl:\t' + real_url)
                if expected_url == real_url:
                    print('pass')
                else:
                    print('fail')
            elif check_type == 'screenContrast':
                img_name = self.name
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
            elif check_type == 'expectedText':
                xpath = check['xpath']
                current_text = self.driver.find_element_by_xpath(xpath).text
                expected_text = check['checkData']
                print('expectedText:\t' + expected_text)
                print('currentText:\t' + current_text)
                if expected_text == current_text:
                    print('pass')
                else:
                    print('fail')

            elif check_type == 'printScreen':
                img_name = self.name
                self.driver.get_screenshot_as_file(
                    "./reportImg/" + img_name + str(self.width) + "x" + str(
                        self.high) + ".jpg")

    def set_case_json(self, case_json):
        self.case_json = case_json

    def begin_test(self):
        self.__parse_case_file()
        resolution_width = self.screen_resolution['width']
        resolution_height = self.screen_resolution['high']
        self.__change_resolution(resolution_width, resolution_height)
        print(u'当前分辨率：' + str(resolution_width) + 'x' + str(resolution_height))
        for browser in self.browsers:
            self.browser = browser
            self.__open_browser(browser)
            for wh in self.browser_window_size:
                self.high = wh['high']
                self.width = wh['width']
                print(self.name)
                print(u"当前浏览器：" + self.browser + u"\t大小：" + str(self.width) + 'x' + str(self.high))
                try:
                    self.driver.set_window_size(self.width, self.high)
                    self.driver.get(self.url)
                    # do actions
                    self.__do_actions()
                    sleep(1)
                    # check
                    self.__do_check()
                except:
                    print('fail on exception')
                    traceback.print_exc()
                    continue
                finally:
                    # self.driver.refresh()
                    self.driver.delete_all_cookies()
            self.driver.quit()

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
