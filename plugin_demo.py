#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.scan import MePlugin
import urlparse


class MeScan(MePlugin):
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
            "name": "",  # 插件的名称
            "product": "",  # 该插件所针对的应用名称,严格按照文档上的进行填写
            "product_version": "",  # 应用的版本号,严格按照文档上的进行填写
            "desc": """

            """,  # 插件的描述
            "author": [""],  # 插件作者
            "ref": [
                {self.ref.url: ""},  # 引用的url
                {self.ref.src: ""},  # src上的案例
            ],
            "type": self.type.injection,  # 漏洞类型
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

    def check(self):
        """
        验证类型，尽量不触发waf规则
        :return:
        """
        pass

    def result(self):
        """
        攻击类型
        :return:
        """
        pass


if __name__ == '__main__':
    from modules.main import main
    main(MeScan())
