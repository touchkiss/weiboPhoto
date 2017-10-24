# coding:utf8

import re
import os
import urllib.request
from sqlhelper import redishelper


class download_img():
    def __init__(self):
        self.redishelper=redishelper.redishelper()
    # 下载图片
    def download_img(self):
        img = self.redishelper.get_downloading_img()  # http://wx2.sinaimg.cn/large/a716fd45ly1fkne2h84wfj20j60lygr6.jpg
        try:
            req = urllib.request.urlopen(r'http://wx2.sinaimg.cn/large/' + img)
            if req.getcode() == 200:
                buf = req.read()
                if len(buf) > 0:
                    f = open(self.get_img_file_path(img), 'wb')
                    f.write(buf)
                    f.close()
                    print('下载了图片' + img)
                    self.redishelper.finish_download_img(img)
                    return
            print(r'下载图片失败%s' % img)
        except:
            print(r'下载图片失败%s' % img)

    # 取得文件路径
    def get_img_file_path(self, img):
        root_path = r'E:\weiboimages'
        for i in img[:5]:
            root_path += r'\\' + i
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        return root_path + r'\\' + img
