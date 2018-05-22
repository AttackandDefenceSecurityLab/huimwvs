#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json

flow_data = {
    "url": 'http://testphp.vulnweb.com/categories.php',
    "method": "GET",
    "domain": "baidu.com",
    "post_data": "requset_data",
    "user_agent": "",
    "cookie": "test",
    "refer": "http//www.baidu.com",
}

a = json.dumps(flow_data)
b = json.loads(a)
