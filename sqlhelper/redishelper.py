# coding:utf8
import redis
from sqlhelper import mysqlhelper
import traceback


class redishelper:
    # 初始化redis
    def __init__(self, connections=5):
        # 创建redis连接池
        self.redispool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.mysqlhelper = mysqlhelper.mysqlhelper(connections)

    # 向redis中插入待爬取的homepage列表
    def insert_new_homepages(self, homepages):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            pipe = r.pipeline(transaction=True)
            for homepage in homepages:
                if not r.sismember('downloaded_homepage', homepage):
                    r.sadd('unget_homepage', homepage)
            pipe.execute()
            return True
        except:
            traceback.print_exc()
            return False

    # 向redis中插入新的用户
    def insert_new_user(self, username, homepage, photopage):
        try:
            new_user_id = self.mysqlhelper.insert_new_user(username, homepage, photopage)
            if new_user_id is None:
                return False
            r = redis.Redis(connection_pool=self.redispool)
            r.hset('photopage_userid', photopage, new_user_id)
            # r.sadd('unget_photopage')
            self.insert_new_photopage(photopage)
            return True
        except:
            traceback.print_exc()
            return False

    # 向redis中插入新的photopage
    def insert_new_photopage(self, photopage):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            r.sadd('unget_photopage', photopage)
            return True
        except:
            traceback.print_exc()
            return False

    # 向redis中插入新图片列表待下载
    def insert_new_imgs(self, imgs, user_id):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            pipe = r.pipeline(transaction=True)
            for img in imgs:
                r.sadd('unget_img', img)
            pipe.execute()
            print('添加了%s张图片等待下载' % str(len(imgs)))
            self.mysqlhelper.insert_new_imgs(user_id, imgs)
            return True
        except:
            traceback.print_exc()
            return False

    # 取得userid
    def get_user_id(self, photopage):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            if not r.hexists('photopage_userid', photopage):
                return None
            else:
                # 这里返回的userid是这种格式b'userid',所以之后使用要去掉前后多余的b''
                return r.hget('photopage_userid', photopage)
        except:
            traceback.print_exc()
            return None

    # 从redis中取得待下载的img
    def get_downloading_img(self):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            if r.scard('unget_img') <= 0:
                return None
            else:
                return str(r.spop('unget_img'))[2:-1]
        except:
            traceback.print_exc()
            return None

    # 完成下载图片，将该记录从redis删除
    def finish_download_img(self, img):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            if r.hexists('unget_img_userid', img):
                user_id = r.hget('unget_img_userid', img)
                self.mysqlhelper.finish_download_img(img)
                r.hdel('unget_img_userid', img)
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False

    # 取得未爬取的homepage
    def get_downloading_homepage(self):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            if r.scard('unget_homepage') <= 0:
                return None
            return str(r.spop('unget_homepage'))[2:-1]
        except:
            traceback.print_exc()
            return None

    # 插入已经下载完的用户主页地址
    def insert_downloaded_homepage(self, homepage):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            r.sadd('downloaded_homepage', homepage)
            return True
        except:
            traceback.print_exc()
            return False

    # 取得未爬取的photopage个数
    def get_downloading_photopage_count(self):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            return r.scard('unget_photopage')
        except:
            traceback.print_exc()
            return 0

    # 取得未下载的img个数
    def get_downloading_imgs_count(self):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            return r.scard('unget_img')
        except:
            traceback.print_exc()
            return 0

    # 取得未爬取的相册地址
    def get_downloading_photopage(self):
        try:
            r = redis.Redis(connection_pool=self.redispool)
            if r.scard('unget_photopage') <= 0:
                return None
            return str(r.spop('unget_photopage'))[2:-1]
        except:
            traceback.print_exc()
            return None
