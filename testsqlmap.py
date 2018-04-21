#coding:utf-8
import sys
sys.path.append('F:\\\xb9\xa4\xbe\xdf\\huimwvs\\modules\\sqlmapsource')
print sys.path
import sqlmap
url="http://demo.aisec.cn/demo/aisec/click_link.php?id=2"
data=['sqlmap.py','-u',url,'--batch','--level=1','--dbms=mysql']
sql=sqlmap.main(data)
#print