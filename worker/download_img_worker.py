# coding:utf8
import threading
import time
from worker import download_img
from sqlhelper import redishelper

class download_img_worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name=r'下载图片')
        self.worker = download_img.download_img()
        self.redish = redishelper.redishelper()

    def run(self):
        while True:
            while self.redish.get_downloading_imgs_count() == 0:
                time.sleep(2)
                print('当前没有待下载的图片，等待2秒')
            self.worker.download_img()
        print('停止下载图片？')