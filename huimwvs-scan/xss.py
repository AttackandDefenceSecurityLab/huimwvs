#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.scan import MePlugin
import urlparse
import urllib
import requests
import base64
from datetime import datetime
import subprocess
import time



class XssScan(MePlugin):
    """
    类名不可修改，而且需要继承于plugin
    """
    def __init__(self,flow_data=0):
        super(self.__class__, self).__init__()
        if flow_data != 0:
            self.flow_data=flow_data  #如果接收到扫描器传入的链接资源，则采用它；否则该程序的链接资源来自测试对象，为测试使用。
        arr = urlparse.urlparse(self.flow_data['url'])
        self.pairs = urlparse.parse_qsl(arr.query)
        self.target=urlparse.urlunsplit((arr.scheme, arr.netloc, arr.path, '', ''))


        self.plugin_info = {
            "name": "xss检测插件",  # 插件的名称
            "product": "带参数的URL",  # 该插件所针对的应用名称,严格按照文档上的进行填写
            "product_version": "*",  # 应用的版本号,严格按照文档上的进行填写
            "desc": """
            针对带有参数的URL检测
            """,  # 插件的描述
            "author": ["huim"],  # 插件作者
            "ref": [
                {self.ref.url: "https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)"},  # 引用的url
                {self.ref.src: "http://www.anquan.us/static/bugs/wooyun-2016-0206756.html"},  # src上的案例
            ],
            "type": self.type.xss,  # 漏洞类型
            "severity": self.level.low,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "target": self.target  #漏洞目标
        }
        self.getparas={}

    def match(self):
        """
        匹配是否调用此插件
        :return:
        """
        return True
    def dynamic_scan(flow_data):
        vulurllist = self.prescan()

        #print vulurllist
        if vulurllist == None:
            return None
        else:
            print datetime.now()
            premethod = 'None'
            dyncookie = 'None'
            dynrequest_data = 'None'
            dynUser_Agent = 'None'
            dynip = 'None'
            dynrefer = 'None'

            if flow_data.has_key('method'):
                dynmethod = flow_data.get('method').strip()
            if flow_data.has_key('cookie'):
                dyncookie = flow_data.get('cookie').strip()
            if flow_data.has_key('request_data'):
                dynrequest_data = flow_data.get('request_data').strip()
            if flow_data.has_key('profilekey'):
                fingerprint = flow_data.get('profilekey').strip()
            else:
                fingerprint = ''
            payloads = ["\"><script>alert(585858)</script><\"", "--></script><script>alert(585858)</script>", "\'};alert(585858);{\'"]



            for scanurls in vulurllist:
                for payload in payloads:
                    scanurl = scanurls.replace("585858xss", payload)
                    # 需要将cookie传给js,通过base64编码字符串实现
                    jsurl = base64.b64encode(scanurl)
                    jsmethod = dynmethod
                    jscookie = base64.b64encode(str(dyncookie))
                    jsrequest_data = base64.b64encode(str(dynrequest_data))

                    # "phantomjs modules/hello.js {url} {method} {cookie} {request_data}"
                    cmd = "phantomjs plugins/hello.js %s %s %s %s" % (jsurl, jsmethod, jscookie, jsrequest_data)
                    # print 'cmd: ', cmd
                    stdout, stderr = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
                    print stdout, stderr
                    vul_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

                    if 'Success' in stdout:
                        vul_type = 'xss'
                        vul_level = '中危'
                        vul_url = scanurl
                        print ('Result:' + vul_time, vul_type, vul_level, vul_url, payload, fingerprint)
                        break
            print datetime.now()

    def check(self):
        """
        验证类型，尽量不触发waf规则
        :return:
        """
        for k,v in self.pairs:
            self.getparas[k]=v
        self.dynamic_scan()
        if self.payloads:
            return True
        pass
    def prescan(self):
        preip = 'None'
        vulurllist = []

        target=self.target
        premethod=self.flow_data['method']
        headers = self.flow_data['head']
        newparas=self.flow_data['newparas'].split('&')
        if premethod.upper() == 'GET':
            inj = "huimxssprescan"
            for key in self.getparas:
                #如果参数不是新出现的，为之前检测过的，那么continue不检测。只检测新出现的参数
                if key not in newparas:
                    continue
                #把参数复制新一份，再一个一个尝试添加
                getparas=self.getparas.copy()
                getparas[key] += inj
                rep=requests.get(target,params=getparas,headers=headers)
                reptext=rep.text
                if "huimxssprescan" in reptext:
                    #		print scanurl
                    #print "-->prescan ok"
                    #print rep.url
                    vulurllist.append(key)
        else:
            return None

        return vulurllist

    def dynamic_scan(self):
        vulurllist = self.prescan()

        #print vulurllist
        if vulurllist == None:
            return None
        else:
            #print datetime.now()
            target = self.target
            dynmethod = self.flow_data.get('method').strip()
            dyncookie = self.flow_data.get('cookie',"None").strip()
            dynrequest_data = self.flow_data.get('request_data',"None").strip()
            fingerprint = self.flow_data.get('profilekey',"").strip()
            payloads = ["\"><script>alert(huimxss)</script><\"", "--></script><script>alert(huimxss)</script>", "\'};alert(huimxss);{\'"]

            for psbkey in vulurllist:
                for payload in payloads:
                    getpara=self.getparas.copy()
                    getpara[psbkey] += payload
                    scanurl = target + '?' + self.changePara(getpara)
                    #print scanurl
                    #scanurl = scanurls.replace("huimxssprescan", payload)
                    # 需要将cookie传给js,通过base64编码字符串实现
                    jsurl = base64.b64encode(scanurl)
                    jsmethod = dynmethod
                    jscookie = base64.b64encode(str(dyncookie))
                    jsrequest_data = base64.b64encode(str(dynrequest_data))

                    # "phantomjs modules/hello.js {url} {method} {cookie} {request_data}"
                    cmd = "phantomjs hello.js %s %s %s %s" % (jsurl, jsmethod, jscookie, jsrequest_data)
                    #cmd = "phantomjs"
                    # print 'cmd: ', cmd
                    #print cmd
                    stdout, stderr = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
                    #print stdout,stderr
                    vul_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

                    if 'Success' in stdout:
                        self.payloads.append(scanurl)
                        self.paras.append(psbkey)
                        break
    def changePara(self,para):
        qs=""
        for key in para:
            val = para[key]
            if qs:
                #qs += "&" + urllib.quote(key) + "=" + urllib.quote(val)
                qs += "&" + key + "=" + val
            else:
                #qs += urllib.quote(key) + "=" + urllib.quote(val)
                qs += key + "=" + val
        return qs

    def result(self):
        """
        攻击类型
        :return:
        """
        pass


if __name__ == '__main__':
    from modules.main import main
    main(XssScan())
