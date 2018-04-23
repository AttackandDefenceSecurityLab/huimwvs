#coding:utf-8
import redis
import json
from csrf import CsrfScan
from sqli import SqliScan
from modules.main import main
import time


r=redis.Redis(host='127.0.0.1',port=6379,db=0)
#while True:
datas=r.lrange('data',-7,-7)
print datas
for data in datas:
    print data
    if data:
        jsonData=json.loads(data)
        exist=main(SqliScan(jsonData)) #传入的字典需要由插件判断是否存在某key，如cookie可能不存在，在进行 data['coookie']提取时会报错
        if exist:
            "[ 检测出存在漏洞 ]"
        else:
            print "不存在"
    else:
        print "NO DATA"
        #time.sleep(10)


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