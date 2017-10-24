# coding:utf8

import pymysql
import time
import traceback
from DBUtils.PooledDB import PooledDB


class mysqlhelper:
    def __init__(self, connections=5):
        pymysql.install_as_MySQLdb()
        # mysql请先创建数据库
        # create database weibo;
        # use weibo;
        # CREATE TABLE `t_user` (
        # `user_id` int(11) NOT NULL AUTO_INCREMENT,
        # `username` varchar(45) NOT NULL,
        # `homepage` varchar(200) NOT NULL,
        # `photopage` varchar(200) NOT NULL,
        # `create_time` bigint(20) NOT NULL,
        # PRIMARY KEY (`user_id`),
        # UNIQUE KEY `user_id_UNIQUE` (`user_id`)
        # ) ENGINE=InnoDB AUTO_INCREMENT=11554 DEFAULT CHARSET=utf8;
        # CREATE TABLE `t_img` (
        # `img_id` varchar(100) NOT NULL,
        #  user_id` int(11) NOT NULL,
        #  `create_time` bigint(20) DEFAULT NULL,
        #  `download_time` bigint(20) DEFAULT NULL,
        #  PRIMARY KEY (`img_id`),
        #  UNIQUE KEY `img_id_UNIQUE` (`img_id`)
        # ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        # 创建连接池
        self.pool = PooledDB(pymysql,
                             connections,
                             host='localhost',
                             user='root',
                             password='mouse',
                             database='weibo',
                             charset='utf8')

    # 取得connection
    def get_conn(self):
        return self.pool.connection()

    # 执行sql
    def execute(self, sql):
        sql.encode('utf8')
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    # 插入新用户
    def insert_new_user(self, username, homepage, photopage):
        sql = "INSERT INTO t_user (username,homepage,photopage,create_time) VALUES ('" + username + "','" + homepage + "','" + photopage + "'," + self.get_now_time() + ")"
        # print(sql)
        # 需要使用utf8转码一下，即使mysql和python都默认utf8编码，不然包含中文的字段不能插入
        sql.encode('utf-8')
        # print(sql)
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        # 取得上一次插入的主键，一定要在commit之前才能取到
        new_user_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return new_user_id

    # 插入新的用户图片
    def insert_new_imgs(self, user_id, imgs):
        try:
            l = len(imgs)
            if l <= 0:
                return
            # sqltext = 'INSERT INTO t_img (img_id,user_id,create_time) VALUES '
            now_time = self.get_now_time()
            l = l - 1
            id = str(user_id)
            print(id[2:-1])
            conn = self.get_conn()
            cursor = conn.cursor()
            for index, img in enumerate(imgs):
                try:
                    # 这里建议将insert语句拆分写，即不写成insert into *** （） values （），（），（）这样，避免其中有错误导致都不能执行
                    sqltext = "INSERT INTO t_img (img_id,user_id,create_time) VALUES ('" + img + "'," + id[
                                                                                                        2:-1] + "," + now_time + ")"
                    sqltext.encode('utf-8')
                    cursor.execute(sqltext)
                    conn.commit()
                except:
                    print('img保存失败' + img)
                    pass
            cursor.close()
            conn.close()
            return True
        except:
            traceback.print_exc()
            return False

    # 取得时间戳，毫秒
    def get_now_time(self):
        return str(int(round(time.time() * 1000)))

    # 完成图片下载
    def finish_download_img(self, img):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(r"UPDATE t_img SET download_time = " + self.get_now_time() + " WHERE img_id = '" + img + "'")
        conn.commit()
        cursor.close()
        conn.close()
