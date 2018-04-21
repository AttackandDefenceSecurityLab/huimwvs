#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wooyaa
@file: data_handler.py
@time: 2018/3/12 下午10:00
@license: Apache Licence
"""
import simplejson as json

flow_data = {
    "url": 'http://g.58.com/user/contactinfo/?PGTID=0d000000-050a-3e75-fc7e-b42d9004fef1&ClickID=1',
    "method": "GET",
    "domain": "i.anjuke.com",
    "post_data": "requset_data",
    "user_agent": "",
    "cookie": "test",
    "refer": "http//m.58.com/zhengding/zufang/?reform=pcfront",
    "cookie": 'id58=c5/nn1o4yOutj3diP8UVAg==; als=0; jr8_t_c_v1=xykm58com.15149496714450.41840872502599136; wmda_uuid=70b63f05bbac31b4b56f0034428f08b2; wmda_new_uuid=1; UM_distinctid=160baad51098d6-0e4d0b2155e3f3-5d1b3316-100200-160baad510aae5; cookieuid=194edb31-03d9-46b4-b1d4-4b7083300700; _ga=GA1.2.655674372.1515580250; city=bj; xxzl_deviceid=rK3lVBCCwxKPl1uqhvCiYA5Idw%2F3lgPqtXBv5JF1ySc7iHgQIdFwqpQV%2Bd1LXd2J; 58tj_uuid=f61b14bc-a09d-4add-8ff3-c5d569899c9a; cookieuid1=c5/n61p4C3qJZgyyFuesAg==; gr_user_id=3d64985e-16f9-4109-9b0e-c8a34dd083a5; 58home=bj; xxzl_smartid=abcf489fc78846bb928a36fd752e0776; wmda_visited_projects=%3B3846689832833%3B1731916484865%3B4166015077506%3B2286118353409%3B2902274187521%3B4166008487938%3B3810569770498%3B3846682473985%3B1732030748417%3B1409632296065%3B1732038237441%3B2385390625025%3B1731918550401; commonTopbar_myfeet_tooltip=end; Hm_lvt_4d4cdf6bc3c5cb0d6306c928369fe42f=1519384062,1519384644,1519384708,1519496932; Hm_lvt_d32bebe8de17afd6738ef3ad3ffa4be3=1519378931,1519496932; gm58lang=zh_CN; bdshare_firstime=1519548765658; TDC_token=3397351790; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1519381213,1519496163,1519580335; Hm_lvt_e15962162366a86a6229038443847be7=1519381213,1519496163,1519580336; gj-manual-guide-top=1; citylistname=gllosangeles; hots=%5B%7B%22d%22%3A0%2C%22s1%22%3A%22%E3%80%90%E6%9E%97%E4%BF%8A%E6%9D%B0%E3%80%91%22%2C%22s2%22%3A%22%E8%AF%9A%E6%B1%82%22%2C%22n%22%3A%22sou%22%7D%5D; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1519496072,1519580339,1519885807,1520308930; __utma=253535702.655674372.1515580250.1520308856.1520330011.11; __utmz=253535702.1520330011.11.9.utmcsr=post.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/hy/postsuccess/0/33322240582194/; final_history=23973891050042%2C33319417758272%2C32858413983296%2C33265769783757%2C33241789734197; new_uv=63; utm_source=; spm=; init_refer=; Hm_lvt_f1527f186a53bd6e02d9e810f8b47b4d=1520235453,1520845687,1520934530,1521740481; _gid=GA1.2.1559420592.1521740481; new_session=0; ppStore_fingerprint=336F76BC9937DFA0E05268233CB738C4B036816640857502%EF%BC%BF1521740677744; PPU="UID=52213474027022&UN=1jrk3mlo3&TT=baf4bd0122b7a7e1d7c95f2559f0d7e5&PBODY=dTF99LgBKfz39uSo3KoP1qjnLrDH5OKnBt6kwRadjYBV9duYqu1_mHqr10sm1w8a8BKtpVe5vUGBtnUjtYmRlfLavPqVA4y-DQ-La8JkbT9VlednGBhZSwcaavMRPWeQd87F56_RCMwnJZnpruhLfHVHRosH6LwmKTAf2epDNWs&VER=1"; 58cooper="userid=52213474027022&username=1jrk3mlo3&cooperkey=d31e34c5f3858efc7b1572e97e21ddc8"; www58com="AutoLogin=false&UserID=52213474027022&UserName=1jrk3mlo3&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=53115061EEDA8F62CA410A5331A86B8706C1D933E76F76B14&Phone=&WltUrl=&UserLoginVer=2A31A22D970634059C5F093E74B4647E7&LT=1521740676903"; Hm_lpvt_f1527f186a53bd6e02d9e810f8b47b4d=1521740678'
}

a = json.dumps(flow_data)
b = json.loads(a)
