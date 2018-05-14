#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.scan import MePlugin
import urlparse
import time
import pycurl


class HashcollisionScan(MePlugin):
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
            "name": "hash碰撞检测插件",  # 插件的名称
            "product": "json等传输POST数据的URL",  # 该插件所针对的应用名称,严格按照文档上的进行填写
            "product_version": "*",  # 应用的版本号,严格按照文档上的进行填写
            "desc": """
            传入hash碰撞数据检测php/java漏洞
            """,  # 插件的描述
            "author": ["huim"],  # 插件作者
            "ref": [
                {self.ref.url: ""},  # 引用的url
                {self.ref.src: ""},  # src上的案例
            ],
            "type": self.type.hashcollision,  # 漏洞类型
            "severity": self.level.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "target": self.target  #漏洞目标
        }

    def match(self):
        """
        匹配是否调用此插件
        :return:
        """
        return True
        # request_data=self.flow_data.get('request_data')
        # if "{" in request_data and "}" in request_data:
        #     return True
        # return False
    def control(self,input_url,data):
        c = pycurl.Curl()
        c.setopt(pycurl.URL,input_url)
        c.setopt(pycurl.POSTFIELDS,  data)
        c.perform()
        http_total_time = c.getinfo(pycurl.TOTAL_TIME)
        return http_total_time
    def check(self):
        """
        验证类型，尽量不触发waf规则
        :return:
        """
        url=self.flow_data['url']
        nulldata=open("null.txt","r").readline()
        normaldata=open("normal.txt","r").readline()
        phpjsondata=open("phpjsonByPython_15_size.txt","r").readline()
        javajsondata=open("javajson.txt","r").readline()


        times={}
        times["null"]=self.control(url,nulldata)
        time.sleep(1)
        times["normal"]=self.control(url,normaldata)  #利用normal，算出发送大量数据的时间，所占比例约为 (normal-null)*4/5
        time.sleep(1)

        #trantime为发送大量数据所占用时间
        trantime=(times["normal"]-times["null"])*4/5

        #base为发送无数据请求+服务器页面运行的时间，约等于服务器页面运算的时间
        base=times["normal"]-trantime

        #根据测算，大于limit界限时间可能存在hash碰撞。
        limit=base*30

        # 根据存放各数据文件的大小，按比例算出大概的发送数据的时间，从整个请求的时间中去除
        times["phpjson"]=self.control(url,phpjsondata)-1.36*trantime
        times["javajson"]=self.control(url,javajsondata)-2.3*trantime

        IfExist=False
        for name in times:
            if times[name]>limit:
                print "Probably have HashCollision==>",
                payload="TYPE : "+name+" SERVER RUNNING TIME : "+str(times[name])
                self.payloads.append(payload)
                IfExist=True
        return IfExist

    def result(self):
        """
        攻击类型
        :return:
        """
        pass


if __name__ == '__main__':
    from modules.main import main
    main(HashcollisionScan())
