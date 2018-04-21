#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse

from scan import LogLevel, VulType, VulLevel


def main(me_instance):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', required=False, action="store_true", help="显示测试信息")
    parser.add_argument('--mode', required=False, default="check", choices=["check", "match"], help="插件离线执行模式, default: verify [str_filed]")

    args = vars(parser.parse_known_args()[0])

    if args['debug']:
        me_instance.log_level = LogLevel.debug
    if args['mode'] == 'match':
        me_instance.match()
    else:
        me_instance.check()

    if me_instance.check:
        print('[插件作者]')
        print('\t{p_author}'.format(p_author=str(me_instance.plugin_info.get('author', ''))))
        print('[风险]')
        print('\t目标 {target} 存在 {p_name}'.format(
            target=str(me_instance.plugin_info.get('target', '')),
            p_name=me_instance.plugin_info.get('type', '').strip()
        ))

        print('[详细说明]')
        print('\t{p_desc}'.format(p_desc=me_instance.plugin_info.get('desc', '').strip()))

        print('[危害等级]')
        print('\t{p_severity}'.format(p_severity=me_instance.plugin_info.get('severity', '')))

        print('[漏洞类别]')
        print('\t{p_type}'.format(p_type=me_instance.plugin_info.get('type', '')))

        print('[相关引用]')
        for each_ref in me_instance.plugin_info.get('ref', {}):
            if not each_ref:
                return

            ref_key = each_ref.keys()[0]
            print('\t* {ref_key}: {ref_value}'.format(ref_key=ref_key, ref_value=each_ref.get(ref_key).strip()))
        return 123 #暂时返回一串测试字符串，信息确定后，修改为返回记录的信息
    else:
        #print('[插件执行失败]: 目标不存在该漏洞 !!!')
        return None
        #me_instance.print_error(me_instance.result.error)


