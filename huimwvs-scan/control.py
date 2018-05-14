#coding:utf-8
import redis
import json
from csrf import CsrfScan
from sqli import SqliScan
from xss import XssScan
from hashcollision import HashcollisionScan
from modules.main import main
import time
import chardet
import threading
import Queue
from public import byteify

r=redis.Redis(host='127.0.0.1',port=6379,db=0)




def check():
    datas=r.lrange('data',0,1)
    for data in datas:
        print data
        if data:
            print "[ ------------- CHECK DATA ------------- ]"
            jsonData=json.loads(data)
            jsonData=byteify(jsonData)
            #print "sql"
            #main(SqliScan(jsonData))
            #print "xss"
            #main(XssScan(jsonData))
            print "csrf"
            main(CsrfScan(jsonData))
            #main(HashcollisionScan(jsonData))
            print "[ ------------- WAITING NEXT ------------- ]"

        else:
            #print "[ ------------- NO DATA ------------- ]"
            time.sleep(10)
def go():
    threadcount=1
    threads=[]
    for i in range(threadcount):
        t=threading.Thread(target=check)
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    go()