#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.scan import MePlugin
import time
import sys
sys.path.append(sys.path[0]+'\\modules\\sqlmapsource')
import sqlmap
import urlparse
import chardet

class SqliScan(MePlugin):
    """
    类名不可修改，而且需要继承于plugin
    """
    def __init__(self,flow_data=0):
        super(self.__class__, self).__init__()
        if flow_data != 0:
            self.flow_data=flow_data  #如果接收到扫描器传入的链接资源，则采用它；否则该程序的链接资源来自测试对象，为测试使用。
            arr = urlparse.urlparse(self.flow_data['url'])
            self.target=urlparse.urlunsplit((arr.scheme, arr.netloc, arr.path, '', ''))
        self.plugin_info = {
            "name": "sql注入检测插件",  # 插件的名称
            "product": "带参数的URL",  # 该插件所针对的应用名称,严格按照文档上的进行填写
            "product_version": "*",  # 应用的版本号,严格按照文档上的进行填写
            "desc": """
            调用sqlmap对url、参数、cookie及Header等进行sql注入检测
            """,  # 插件的描述
            "author": "[huim]",  # 插件作者
            "ref": [
                {self.ref.url: "https://www.owasp.org/index.php/SQL_Injection"},  # 引用的url
                {self.ref.src: "http://www.anquan.us/static/bugs/wooyun-2016-0219921.html"},  # src上的案例
            ],
            "type": self.type.injection,  # 漏洞类型
            "severity": self.level.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "target": self.target  #漏洞目标
        }
        #print type(self.plugin_info['author'])
        #print chardet.detect(self.plugin_info.get('target',""))
    def match(self):
        """
        匹配是否调用此插件
        :return:
        """
        method=self.flow_data['method']
        url=self.flow_data['url']
        # GET需要有? = 带参特征
        if method=='GET':
            if '?' in url and '=' in url:
                return True
            else:
                return False
        #POST 需要有data 带参特征
        else:
            # 虽然前段已验证只发送带参数的POST数据，但此处严谨过滤较好
            if ('?' in url and '=' in url) or self.flow_data.get('request_data'):
                return True
            else:
                return False

    def check(self):
        """
        验证类型，尽量不触发waf规则
        :return:
        """

        #url, premethod, cookie, prerequest_data, preUser_Agent, preip, prerefer = head_info_get(data, flag)
        url=self.flow_data['url']
        #print chardet.detect(url)
        newparas=self.flow_data['newparas'].split('&')
        method=self.flow_data['method']
        cookie=self.flow_data.get('cookie',"")
        ua_string=self.flow_data.get('User-Agent',"")
        request_data=self.flow_data.get('request_data',"")
        #print url
        '''
        标记新参数，即需要检测的参数
        GET参数：对url ?X=  &X=特征的参数加*
        POST参数：符合的参数加*
        URI 与 POST 用来存放 sqlmap 结果"#1* (URI)"类对应的参数，在后面转换
        '''
        URI=[]
        POST=[]
        for newpara in newparas:
            if newpara in url:
                url=url.replace('?'+newpara+'=','?'+newpara+'=*')
                url=url.replace('&'+newpara+'=','&'+newpara+'=*')
                URI.append(newpara)
            if newpara in request_data:
                request_data=request_data.replace(newpara+'=',newpara+'=*')
                POST.append(newpara)
        #print url
        if cookie:
            data=['sqlmap.py','-u',url,'--batch','--level=1','--dbms=mysql','--cookie',cookie,'--user-agent',ua_string]
        else:
            data=['sqlmap.py','-u',url,'--batch','--level=1','--dbms=mysql','--user-agent',ua_string]
        if request_data:
            data.append('--data')
            data.append(request_data)
        try:
            injection=sqlmap.main(data)
        # except Exception, e:
        #     #pass
        #     print "[ERROR] : ",
        #     print Exception,
        #     print "[INFO] : ",
        #     print e
        #     #return
        except:
            pass


        if injection and str(injection.get('data','not found')).find("Payload")!=-1:
            rows=str(injection.get('data','not found')).split("\n")
            for row in rows:
                if "Payload" in row:
                    payload=row.split(": ")[1]
                    self.payloads.append(payload)
                if "Parameter:" in row:
                    prepara = row.split(": ")[1]
                    #prepare如 "#1* (URI)"
                    if "URI" in prepara:
                        # prepare由此截取出一个数字
                        prepara=prepara.split("#")[1].split("*")[0]
                        para = URI[int(prepara)-1] + "(GET)"
                        #print chardet.detect(URI[int(prepara)-1])
                    elif "POST" in prepara:
                        prepara=prepara.split("#")[1].split("*")[0]
                        para = POST[int(prepara)-1] + "(POST)"
                    self.paras.append(para)

            return True
            #file_data="success: [",vul_time,"] url:",url," payload:",payload," cookie:",cookie,"","\n"

    def result(self):
        """
        攻击类型
        :return:
        """
        pass


if __name__ == '__main__':
    from modules.main import main
    main(SqliScan())
