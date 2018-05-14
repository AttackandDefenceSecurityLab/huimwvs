#coding:utf-8
import redis
import json
from public import byteify
from time import sleep
r=redis.Redis(host='127.0.0.1',port=6379,db=0)
while True:
    data=r.lpop('data')
    #print data
    if data:
        jsonData=json.loads(data)
        jsonData=byteify(jsonData)
        if "bilibili" in jsonData['url']:
            sleep(0.2)
            print "DELETE BILIBILI"
            pass
        else:
            r.rpush('data',data)
    else:
        break