from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import queue
import os
import sys
import platform

class Headless:

    def __init__(self, path):
        '''
        队列策略默认先进先出;
        :param path: 无头浏览器路径
        '''
        self.path = self.format_path(path)
        self.queue = queue.Queue()

    def format_path(self, path):
        '''
        查找目录下所有无头浏览器,浏览器前缀必须:driver
        :path: 存放目录
        :return:
        '''
        path_list = []
        if not os.path.exists(path): return
        for file in os.listdir(path):
            if 'driver' in file:
                path_new = os.path.join(path, file)
                path_list.append(path_new)
        return path_list

    def init_object(self, path):
        '''
        初始化无头对象,默认无头,默认禁止图片和css加载
            设置 chrome 二进制文件位置 (binary_location)
            添加启动参数 (add_argument)
            添加扩展应用 (add_extension, add_encoded_extension)
            添加实验性质的设置参数 (add_experimental_option)
            设置调试器地址 (debugger_address)
        :return:
        '''
        options = Options()
        options.add_argument('--headless')
        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        options.add_experimental_option('prefs', prefs)

        options.add_experimental_option('excludeSwitches'['enable-automation'])
        driver = webdriver.Chrome(executable_path=path, options=options)
        return driver

    def run(self):
        '''
        将无头object添加到队列
        :return: 队列
        '''
        for path in self.path:
            diriver = self.init_object(path)
            if diriver:
                self.queue.put(diriver)
        return self.queue

    def is_ios(self):
        '''
        判断代码运行环境
        :return:
        '''
        ios_name = sys.platform
        if ios_name == 'win32':
            return 'w'
        elif ios_name == 'linux':
            return 'l'
        elif ios_name == 'darwin':
            return 'm'
        else:
            return '无法识别运行环境'

    def get_cookie(self, driver, url):
        '''
        获取网站cookie
        :param driver: 对象
        :param url: 网址
        :return: driver, 'cookie'
        '''
        driver.get(url)
        cookies = ''
        for i in driver.get_cookies():
            if i['name'] == 'JSESSIONID':
                cookie = '{name}={value};'.format(name=i['name'], value=i['value'])
                cookies = cookies + cookie
        return driver, cookies
