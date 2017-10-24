# coding:utf8
from worker import homepage_worker,photopage_worker,download_img_worker


if __name__ == '__main__':
    homepage_worker1=homepage_worker.homepage_worker()
    homepage_worker2=homepage_worker.homepage_worker()
    homepage_worker3=homepage_worker.homepage_worker()
    photopage_worker=photopage_worker.photopage_worker()
    download_img_worker1=download_img_worker.download_img_worker()
    download_img_worker2=download_img_worker.download_img_worker()
    download_img_worker3=download_img_worker.download_img_worker()
    download_img_worker4=download_img_worker.download_img_worker()
    download_img_worker5=download_img_worker.download_img_worker()

    # 开工
    homepage_worker1.start()
    homepage_worker2.start()
    homepage_worker3.start()
    photopage_worker.start()
    download_img_worker1.start()
    download_img_worker2.start()
    download_img_worker3.start()
    download_img_worker4.start()
    download_img_worker5.start()