#coding:utf-8
import sys
sys.path.append('F:\\\xb9\xa4\xbe\xdf\\huimwvs\\modules\\sqlmapsource')
print sys.path
import sqlmap
url="http://demo.aisec.cn/demo/aisec/js_link.php?id=1&msg=abc"
data=['sqlmap.py','-u',url,'--batch','--level=1','--dbms=mysql']
sql=sqlmap.main(data)
print "-------------------------------------"
payloads=sql['data'].split('\n')
for payload in payloads:
    #print payload
    if 'Payload' in payload:
        print payload.split(': ')[1]