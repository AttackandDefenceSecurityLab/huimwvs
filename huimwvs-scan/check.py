#coding:utf-8
import redis
import json
from csrf import CsrfScan
from sqli import SqliScan
from modules.main import main
import time
import chardet
from public import byteify

r=redis.Redis(host='127.0.0.1',port=6379,db=0)
datas=r.lrange('data',0,-1)
#print datas
#while True:
print len(datas)
for data in datas:
    #print data
    if data:
        jsonData=json.loads(data)
        jsonData=byteify(jsonData)
        #print jsonData['url']
        #print jsonData['newparas']





