#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
import chardet
from public import pool
from scan import LogLevel, VulType, VulLevel


def main(me_instance):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', required=False, action="store_true", help="显示测试信息")

    args = vars(parser.parse_known_args()[0])
    if args['debug']:
        me_instance.log_level = LogLevel.debug
    """
    检测是否匹配，不匹配则不存在该漏洞，返回None
    """
    if me_instance.match():
        """
        如果匹配，调用检测方法
        """
        if me_instance.check():
            sql={}
            sql["userid"]="1"

            print('[插件作者]')
            print('\t{p_author}'.format(p_author=str(me_instance.plugin_info.get('author', ''))))
            #sqlkey += "plugin_author,"
            #sqlvalue += "\""+str(me_instance.plugin_info.get('author', ''))+"\","
            sql["plugin_author"]=str(me_instance.plugin_info.get('author', ''))
            #print type(me_instance.plugin_info['author'])
            print('[风险]')
            print('\t目标 {target} 存在 {p_name}'.format(
                target=str(me_instance.plugin_info.get('target', '')),
                p_name=me_instance.plugin_info.get('type', '').strip()
            ))
            #sqlkey += "target,"
            #sqlvalue += "\""+str(me_instance.plugin_info.get('target', '')) + "\","
            sql["target"]=str(me_instance.plugin_info.get('target', ''))

            #sqlkey += "url,"
            #print chardet.detect(me_instance.flow_data['url'])
            #sqlvalue += "\""+me_instance.flow_data['url'] + "\","
            sql["url"]=me_instance.flow_data['url']
            #sqlkey += "vultype,"
            #sqlvalue += "\""+str(me_instance.plugin_info.get('type', ''))+"\","
            sql["vultype"]=str(me_instance.plugin_info.get('type', ''))

            if me_instance.paras:
                print('[参数]')
                print('\t'),
                #sqlkey += "para,"
                paravalue = ""
                for para in me_instance.paras:
                    print(('{p_para} ').format(p_para=para)),
                    #print "para编码"
                    #print chardet.detect(para)
                    paravalue += para + " "
                sql["para"]=paravalue
                #print('')

            print('[详细说明]')
            print('\t{p_desc}'.format(p_desc=me_instance.plugin_info.get('desc', '').strip()))
            #sqlkey += "descrip,"
            #sqlvalue += "\""+me_instance.plugin_info.get('desc', '').strip() + "\","
            sql["descrip"]=me_instance.plugin_info.get('desc', '').strip()

            print('[危害等级]')
            print('\t{p_severity}'.format(p_severity=me_instance.plugin_info.get('severity', '')))
            #sqlkey += "severity,"
            #sqlvalue += "\""+me_instance.plugin_info.get('severity', '') + "\","
            sql["severity"]=me_instance.plugin_info.get('severity', '')

            print('[漏洞类别]')
            print('\t{p_type}'.format(p_type=me_instance.plugin_info.get('type', '')))

            if me_instance.payloads:
                #sqlkey += "payload,"
                pocvalue =""
                print('[漏洞POC]')
                for payload in me_instance.payloads:
                    pocvalue += "<" + payload + ">"
                    print(('\t{p_poc}').format(p_poc=payload))
                sql["payload"]=pocvalue
                #sqlvalue += "\","

            print('[相关引用]')
            if me_instance.plugin_info.get('ref', {}):
                #sqlkey += "ref"
                refvalue = ""
                for each_ref in me_instance.plugin_info.get('ref', {}):
                    if not each_ref:
                        return
                    ref_key = each_ref.keys()[0]
                    print('\t* {ref_key}: {ref_value}'.format(ref_key=ref_key, ref_value=each_ref.get(ref_key).strip()))
                    refvalue += "<"+ref_key + ":" + each_ref.get(ref_key).strip()+">"
                sql["ref"]=refvalue
                #sqlvalue += "\""
            #sql = "INSERT INTO vul ({keys}) VALUES ({vaules})".format(keys=sqlkey,vaules=sqlvalue)
            #print sql
            inrep=pool.insert("vul",sql)
            if inrep:
                print "[ SUCCESS INSERT ]"
            return 123
        else:
            #print('[插件执行失败]: 目标不存在该漏洞 !!!')
            return None
            #me_instance.print_error(me_instance.result.error)
    else:
        return None

