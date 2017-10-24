# coding:utf8
import threading
import time
from browser_control import browser_controler
from sqlhelper import redishelper

class photopage_worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name=r'访问用户相册')
        self.worker = browser_controler.browser_controler()
        self.redish = redishelper.redishelper()

    def run(self):
        while True:
            while self.redish.get_downloading_photopage_count() == 0:
                time.sleep(2)
                print('当前没有待爬取的相册，等待2秒')
            self.worker.match_user_imgs(self.redish.get_downloading_photopage())
