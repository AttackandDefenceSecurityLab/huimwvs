#coding:utf-8
import redis
import json
from csrf import CsrfScan
from modules.main import main
import time

r=redis.Redis(host='127.0.0.1',port=6379,db=0)
while True:
    data=r.lpop('data')
    #print data
    if data:
        jsonData=json.loads(data)
        csrf=main(CsrfScan(jsonData))
        if csrf:
            print csrf
        else:
            print "no csrf"
    else:
        print "NO DATA"
        time.sleep(10)


# datas=r.lrange('data',0,-1)
# for data in datas:
#     if len(data) != 0:
#         jd=json.loads(data)
#         try:
#             #print jd['method']
#             print jd['url']
#             csrf=main(CsrfScan(jd))
#             if csrf:
#                 print csrf
#             else:
#                 print "不存在csrf"
#         except:
#             pass
#         print



# test=r.lrange('data',0,1)
# jd=json.loads(test[1])

# csrf=main(CsrfScan(jd))
# if csrf:
#     print csrf
# else:
#     print "不存在csrf"