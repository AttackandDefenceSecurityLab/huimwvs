import requests
import urllib
para={'a':'1','b':'2','c':'3'}
def changePara(para):
    qs=""
    for key in para:
        val = para[key]
        if qs:
            qs += "&" + urllib.quote(key) + "=" + urllib.quote(val)
        else:
            qs += urllib.quote(key) + "=" + urllib.quote(val)
    return qs
print changePara(para)