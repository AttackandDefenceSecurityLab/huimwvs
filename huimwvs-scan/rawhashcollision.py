#coding:utf-8
import time
import pycurl



# def timeOfRequest(url,data):
#     start=time.time()
#     #print data
#     try:
#         q=requests.post(url,data)
#         #print q.content
#         return q.elapsed.total_seconds()
#     except:
#         pass
#     end=time.time()
#     return 1000000
#     #return (end-start)

def control(input_url,data):
        c = pycurl.Curl()
        c.setopt(pycurl.URL,input_url)
        c.setopt(pycurl.POSTFIELDS,  data)
        c.perform()
        http_total_time = c.getinfo(pycurl.TOTAL_TIME)
        return http_total_time

def show(times,limit):
    for name in times:
        if times[name]>limit:
            print "Probably have HashCollision==>",
        print name+":",
        print times[name]

def check(url):
    nulldata=open("null.txt","r").readline()
    normaldata=open("normal.txt","r").readline()
    phpjsondata=open("phpjsonByPython_15_size.txt","r").readline()
    javajsondata=open("javajson.txt","r").readline()


    times={}
    times["null"]=control(url,nulldata)
    time.sleep(1)
    times["normal"]=control(url,normaldata)  #利用normal，算出发送大量数据的时间，所占比例约为 (normal-null)*4/5
    time.sleep(1)

    #trantime为发送大量数据所占用时间
    trantime=(times["normal"]-times["null"])*4/5

    #base为发送无数据请求+服务器页面运行的时间，约等于服务器页面运算的时间
    base=times["normal"]-trantime

    #根据测算，大于limit界限时间可能存在hash碰撞。
    limit=base*30

    # 根据存放各数据文件的大小，按比例算出大概的发送数据的时间，从整个请求的时间中去除
    times["phpjson"]=control(url,phpjsondata)-1.36*trantime
    times["javajson"]=control(url,javajsondata)-2.3*trantime

    for name in times:
        if times[name]>limit:
            print "Probably have HashCollision==>",
            print name+":",
            print times[name]


if __name__ == '__main__':
    url="http://203.195.164.69/tt.php"
    check(url)
