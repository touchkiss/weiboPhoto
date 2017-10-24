# coding:utf8
import threading
import time
from browser_control import browser_controler

class homepage_worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name=r'搜索用户主页地址')
        self.worker = browser_controler.browser_controler()

    def run(self):
        # 从weibo主页开始爬取
        self.worker.start('http://weibo.com')
