#coding:utf-8
import threading
from testdef import tt
threads=[]
for i in range(10000):
    threads.append(threading.Thread(target=tt,args=(i,)))
for t in threads:
    t.start()