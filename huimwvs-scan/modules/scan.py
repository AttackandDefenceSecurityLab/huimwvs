#!/usr/bin/env python
# -*- coding: utf-8 -*-


import colorama
from abc import ABCMeta, abstractmethod
from data_handler import flow_data
colorama.init()


class MeRef(object):
    """
    引用相关
    """
    url = "相关链接"
    src = "SRC案例"


class VulLevel(object):
    """
    危害等级
    """
    critical = '严重'
    high = '高危'
    medium = '中危'
    low = '低危'
    bug = 'BUG'


class LogLevel(object):
    """
    日志级别
    """
    debug = 1
    info = 2
    warning = 3
    error = 4


class VulType(object):
    """
    漏洞类型
    """
    lfi = '本地文件包含'
    rfi = '远程文件包含'
    injection = 'sql注入'
    xss = 'xss跨站脚本攻击'
    xxe = 'xml外部实体攻击'
    rce = '远程命令/代码执行'
    info_leak = '信息泄漏'
    file_upload = '任意文件上传'
    file_traversal = '目录遍历'
    file_operation = '任意文件操作'
    misconfiguration = '错误配置'
    business_logic_vul = '业务逻辑漏洞'
    csrf = '跨站请求伪造'
    other = '其他'


class MePlugin(object):
    __metaclass__ = ABCMeta

    ref = MeRef()
    type = VulType()
    level = VulLevel()

    def __init__(self):
        super(MePlugin, self).__init__()
        self.log_level = LogLevel.info
        self.flow_data = flow_data
        self.payloads=[]
        self.paras=[]


    @abstractmethod
    def match(self):
        pass

    @abstractmethod
    def check(self):
        pass

    @staticmethod
    def is_sanbox():
        import os
        if os.environ.get('APP_NAME', None):
            return True

    def print_debug(self, content):
        if self.log_level <= LogLevel.debug:
            if self.is_sanbox():
                print("{content}".format(content=content))
            else:
                print("{debug_color}[debug]: {content} {color_reset}".format(
                    debug_color=colorama.Fore.CYAN, content=content, color_reset=colorama.Fore.RESET))

    def print_info(self, content):
        if self.log_level <= LogLevel.info:
            if self.is_sanbox():
                print("{content}".format(content=content))
            else:
                print("{info_color}[info]: {content} {color_reset}".format(
                    info_color=colorama.Fore.GREEN, content=content, color_reset=colorama.Fore.RESET))

    def print_warning(self, content):
        if self.log_level <= LogLevel.warning:
            if self.is_sanbox():
                print("{content}".format(content=content))
            else:
                print("{warning_color}[warning]: {content} {color_reset}".format(
                    warning_color=colorama.Fore.YELLOW, content=content, color_reset=colorama.Fore.RESET))

    def print_error(self, content):
        if self.log_level <= LogLevel.error:
            if self.is_sanbox():
                print("{content}".format(content=content))
            else:
                print("{error_color}[error]: {content} {color_reset}".format(
                    error_color=colorama.Fore.RED, content=content, color_reset=colorama.Fore.RESET))
