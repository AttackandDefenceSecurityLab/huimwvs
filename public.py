#coding:utf-8
import MySQLdb
from DBUtils.PooledDB import PooledDB
'''
json.loads 数据将为unicode格式
该函数迭代将数据转化为utf-8
'''
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


"""
定义数据库连接池对象，用于其他模块使用
一次import，对象多次使用
"""
#pool = PooledDB(MySQLdb,maxconnections=10000,host='localhost',user='root',passwd='root',db='huimwvs',port=3306) #5为连接池里的最少连接数
class MySQLPool():
    def __init__(self):
        self.pool = PooledDB(MySQLdb,maxconnections=10000,host='localhost',user='root',passwd='root',db='huimwvs',port=3306) #5为连接池里的最少连接数

    def insert(self,table,sqldata):
        sql="INSERT INTO "+table+" "
        keys=""
        values=""
        for key in sqldata:
            keys += key+","
            values += "\"" + sqldata[key] + "\","
        sql += "(" + keys[:-1] + ") VALUES (" + values[:-1] + ")"

        try:
            conn = self.pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
            cur=conn.cursor()
            exrep=cur.execute(sql)
            cur.close()
            conn.close()
            return exrep
        except Exception,err:
            print "[ERROR] : ",
            print Exception,
            print "[INFO] : ",
            print err

pool=MySQLPool()