import sqlmap
import time
import sys
sys.path.append('../modules/sqlmapsource')
def match(data):
    if data['is_keyvalue']:
        return True
    else:
        return False

#def cheak(url,cookie):
def check(data, flag):
    '''
    url=data['url']
    if data.has_key('cookie'):
        cookie=data['cookie']
    else:
        cookie = ""
    '''
    url, premethod, cookie, prerequest_data, preUser_Agent, preip, prerefer = head_info_get(data, flag)

    vul_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    if cookie:
        data=['sqlmap.py','-u',url,'--batch','--level=1','--dbms=mysql','--cookie',cookie,'--user-agent',ua_string]
    else:
        data=['sqlmap.py','-u',url,'--batch','--level=1','--dbms=mysql','--user-agent',ua_string]
    vul_type="sqli"
    vul_level="高危"
    payload=""
    try:
        injection=sqlmap.main(data)
    except Exception, e:
        print e
        return
    print injection
    if injection and str(injection.get('data','not found')).find("payload"):
        payloads=str(injection.get('data','not found')).split(",")
        for payload in payloads:
            if "\'payload\':" in payload:
                payload=payload.split(":")[1].split("'")[1]
        file_data="success: [",vul_time,"] url:",url," payload:",payload," cookie:",cookie,"","\n"
        writefile(file_data)
        #result(vul_time,vul_type,vul_level,url,payload)
def writefile(data):
    try:
        file=open('./sqli_result','a+')
        file.writelines(data)
        file.close()
    except Exception,e:
        print e
def result(vul_time,vul_type,vul_level,vul_url,payload):
    return


if __name__=="__main__":
    cookie=""
    urls=["http://demo.aisec.cn/demo/aisec/click_link.php?id=2","http://demo.aisec.cn/demo/aisec/js_link.php?id=1&msg=abc"]
    for url in urls:
        print url
        check(url,cookie)