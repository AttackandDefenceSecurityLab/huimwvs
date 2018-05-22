#coding:utf-8
import redis
import json
import os
from csrf import CsrfScan
from sqli import SqliScan
from xss import XssScan
from hashcollision import HashcollisionScan
from modules.main import main
import time
import threading
from public import byteify

r=redis.Redis(host='127.0.0.1',port=6379,db=0)

class Watcher():  
  
    def __init__(self):  
        self.child = os.fork()  
        if self.child == 0:  
            return  
        else:  
            self.watch()  
  
    def watch(self):  
        try:  
            os.wait()  
        except KeyboardInterrupt:  
            self.kill()  
        sys.exit()  
  
    def kill(self):  
        try:  
            os.kill(self.child, signal.SIGKILL)  
        except OSError:  
            pass  


def check():
    datas=r.lrange('data',0,-1)
    for data in datas:
        if data:
            print "[ ------------- CHECK DATA ------------- ]"
            jsonData=json.loads(data)
            jsonData=byteify(jsonData)
            #print "CHECKING SQLI"
            #main(SqliScan(jsonData))
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
    Watcher() 
    go()
