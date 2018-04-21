#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wooyaa
@file: plugin_demo.py
@time: 2018/1/22 下午4:28
@license: Apache Licence
"""
from modules.scan import MePlugin


class MeScan(MePlugin):
    """
    类名不可修改，而且需要继承于plugin
    """
    def __init__(self):
        super(self.__class__, self).__init__()
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
        }

    def match(self):
        """
        匹配是否调用此插件
        :return:
        """
        pass

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
