#coding:utf-8
import redis
import json
from csrf import CsrfScan
from sqli import SqliScan
from xss import XssScan
from hashcollision import HashcollisionScan
from modules.main import main
import time
import threading
from public import byteify

r=redis.Redis(host='127.0.0.1',port=6379,db=0)




def check():
    while 1:
        data=r.lpop('data')
        if data:
            print "[ ------------- CHECK DATA ------------- ]"
            jsonData=json.loads(data)
            jsonData=byteify(jsonData)
            print "CHECKING SQLI"
            main(SqliScan(jsonData))
            print "CHECKING XSS"
            main(XssScan(jsonData))
            print "CHECKING CSRF"
            main(CsrfScan(jsonData))
            print "CHECKING HASHCOLLISISON"
            main(HashcollisionScan(jsonData))
            print "[ ------------- WAITING NEXT ------------- ]"

        else:
            time.sleep(10)
def go():
    threadcount=10
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