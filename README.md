# weiboPhoto
咳咳，首先说一下，本教程只是个初始入门级别。

先说一下我的实现方式和用到的一些技术、工具。
##selenium
使用selenium驱动Chrome浏览器访问微博网页，得到网页代码交给 beautifulsoup解析，从中分析出各种信息。共有三种线程：访问用户主页得到用户信息和用户相册地址；访问用户相册得到图片地址；下载图片。
##chrome
Chrome浏览器（Firefox也可以，其实IE啥的也可以 ），自行百度下载chromedriver，（这是一个驱动Chrome浏览器的工具），下载地址：

http://chromedriver.storage.googleapis.com/index.html

，下载后将解压到的chromedriver.exe放到 C:\Users\Windows\AppData\Local\Google\Chrome\Application目录下 
##redis
redis（一种算是数据库吧，用来存储一些临时数据，恰好解决了多线程问题），下载地址

https://github.com/MicrosoftArchive/redis/releases

，安装即可，然后看这个

http://blog.csdn.net/u010982856/article/details/51658184

将redis设为开机启动
##mysql 
mysql（一种常规数据库，用来存储用户信息），下载地址

https://dev.mysql.com/downloads/mysql/
##python
python（主要用到的编程语言，因为最近一个月才开始看python，所以使用上还是很生疏，也可以用java代替），下载地址

https://www.python.org/downloads/

，建议使用python3 以上版本。记得将C:\Users\你的用户名\AppData\Local\Programs\Python\Python36\Scripts 添加到系统环境变量PATH中，以便运行pip命令。
##接下来安装一些python第三方库
按windows+R输入cmd回车，然后键入以下命令安装

pip install wheel

pip install mysqlclient

pip install mysql-connector==2.1.4

pip install pymysql

pip install beautifulsoup4

pip install redis

pip install selenium

pip install DBUtils

pip install lxml
