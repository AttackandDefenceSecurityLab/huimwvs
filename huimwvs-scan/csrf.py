#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.scan import MePlugin


class CsrfScan(MePlugin):
    """
    类名不可修改，而且需要继承于plugin
    """
    def __init__(self,flow_data=0):
        super(self.__class__, self).__init__()
        if flow_data != 0:
            self.flow_data=flow_data  #如果接收到扫描器传入的链接资源，则采用它；否则该程序的链接资源来自测试对象，为测试使用。
        self.plugin_info = {
            "name": "csrf检测插件",  # 插件的名称
            "product": "通用URL",  # 该插件所针对的应用名称,严格按照文档上的进行填写
            "product_version": "*",  # 应用的版本号,严格按照文档上的进行填写
            "desc": """
            主要针对页面中含有form表单的URL，检测POST型form表单
            """,  # 插件的描述
            "author": "huim",  # 插件作者
            "ref": [
                {self.ref.url: "https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)"},  # 引用的url
                {self.ref.src: "http://www.anquan.us/static/bugs/wooyun-2015-095332.html"},  # src上的案例
            ],
            "type": self.type.csrf,  # 漏洞类型
            "severity": self.level.medium,  # 漏洞等级
            "privileged": True,  # 是否需要登录
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
        import requests
        import re
        '''
        获取URL中的表单
        '''


        class csrfCheck:
            '''
            输入原生cookie，返回cookie拆分成的字典类型
            '''
            def tranCookie(self,rawC):
                '''将原生的一大串cookie（从Burpsuite中截取出来）转换为字典'''
                cookie={}
                cookies=rawC.split("; ")
                for i in cookies:
                    cookiedata=i.split("=",1)
                    name=cookiedata[0]
                    if len(cookiedata)>1:
                        value=cookiedata[1]
                    else:
                        value=""
                    cookie[name]=value
                return cookie

            def getForms(self,url,cookie):
                '''输入url与cookie字典，返回页面中的表单html代码 数组'''


                headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
                try:
                    q=requests.get(url,headers=headers,cookies=cookie)
                    rep=q.content
                except:
                    return []
                #print rep

                try:
                    q_nocookie=requests.get(url,headers=headers)
                    rep_nocookie=q_nocookie.content
                except:
                    return []

                forms=re.findall("<form[\s\S]*?</form>",rep)

                # 对比各个表单在没有cookie的情况下是否存在
                # 如果不用cookie也能获取表单
                # 那么csrf没意义，不是需要检测的form，过滤掉
                for i in forms:
                    link=re.findall("<form[\s\S]*?>",i)[0]

                    if link in rep_nocookie:
                        forms.remove(i)
                        print "goout 1"


                '''
                以同样的url和cookie请求，检测在两次请求中表单是否有变化。
                如果有变化，则应该是token每次刷新页面都不同的原因引起的。
                所以排除掉。
                后续如果发现其他引起form变化的非token因素，修改此过滤条件。
                '''
                try:
                    q_recheckToken=requests.get(url,headers=headers,cookies=cookie)
                    rep_recheckToekn=q_recheckToken.content
                except:
                    return []

                for form in forms:
                    if form not in rep_recheckToekn:
                        forms.remove(form)
                        print "goout 2"



                return forms


            def filter(self,forms):
                '''根据条件过滤去大概率不存在csrf的表单'''
                '''去除没有提交按钮的表单'''
                for form in forms:
                    if "submit" not in form.lower() and "button" not in form.lower() and "save" not in form.lower() and "modify" not in form.lower():
                        forms.remove(form)
                        print "goout 3"
                    #print form.lower()

                '''去除带验证码的表单'''
                yzmFile=open("yzm.txt","r")
                yzmtext=yzmFile.readlines()
                yzmFile.close()
                #遍历表单
                for form in forms:
                    #是否有验证码的标记位
                    ifVcode=0
                    imgs=re.findall("<img.*?>",form)
                    #遍历表单中的图片标签
                    for img in imgs:
                        if ifVcode==1:
                            break
                        #遍历关键字对图片标签进行检测
                        for key in yzmtext:
                            #转换为小写字母，不区分大小写
                            if key.strip() in img.lower():
                                forms.remove(form)
                                print "goout 4"
                                ifVcode=1
                                break

                '''去除placeholder（input中的预期信息）符合黑名单的'''
                '''在验证cookie有无影响时已经去除了一遍，这里双重验证'''
                phFile=open("placeholder.txt","r")
                phtext=phFile.readlines()
                phFile.close()
                for form in forms:
                    #placeholder是否符合黑名单的标记位
                    ifPlaceholder=0
                    phs=re.findall("placeholder=\".*?\"",form)
                    #遍历表单中的placeholder属性
                    for ph in phs:
                        if ifPlaceholder==1:
                            break
                        #遍历关键字对placeholder进行检测
                        for key in phtext:
                            #转换为小写字母，不区分大小写
                            if key.strip() in ph.lower():
                                forms.remove(form)
                                print "goout 5"
                                ifPlaceholder=1
                                break

                '''去除cgi中存在search login等黑名单的表单'''
                '''在验证cookie有无影响时已经去除了一遍，这里双重验证'''
                cgiFile=open("cgi.txt","r")
                cgitext=cgiFile.readlines()
                cgiFile.close()
                for form in forms:
                    #cgi是否符合黑名单的标记位
                    ifCgi=0
                    formTitle=re.findall("<form[\s\S]*?>",form)[0]
                    cgis=re.findall("\".*?\"",formTitle)
                    for cgi in cgis:
                        if ifCgi==1:
                            break
                        for key in cgitext:
                            if key.strip() in cgi.lower():
                                forms.remove(form)
                                print "goout 6"
                                ifCgi=1
                                break

                '''
                检测是否存在token的关键字，后续应该将检测的地方定位到更精确的位置
                缩小检测范围，减少漏报
                '''
                tokenFile=open("token.txt","r")
                tokentext=tokenFile.readlines()
                tokenFile.close()
                #检测token关键字
                for form in forms:
                    for key in tokentext:
                        if key.strip() in form.lower():
                            forms.remove(form)
                            print "goout 7"
                            break

            def show(self,forms):
                for form in forms:
                    print form
            def check(self,url,rawCookie):

                cookie=self.tranCookie(rawCookie)
                forms=self.getForms(url,cookie)
                self.filter(forms)
                return forms
        #if __name__ == '__main__':
        req_data = self.flow_data
        url = req_data['url']
        #print url
        try: # 请求中可能不存在cookie，提取字典时会导致报错；如果没有cookie，则设置为空
            cookie = req_data['cookie']
        except:
            ##print "无COOKIE ————————————————"
            cookie=""
        #print cookie
        csrf=csrfCheck()
        forms=csrf.check(url,cookie)
        #print forms
        if len(forms) == 0:
            return False
        else:
            #print url
            for form in forms:
                #self.plugin_info["target"] += "  --  表单："
                payload = re.findall("<form[\s\S]*?>",form)[0]
                self.payloads.append(payload)
            return True
            #csrf.show(result)

    def result(self):
        """
        攻击类型
        :return:
        """
        pass


if __name__ == '__main__':
    #print "你好"
    from modules.main import main
    main(CsrfScan())
