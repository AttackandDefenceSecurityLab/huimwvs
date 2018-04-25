#coding:utf-8
from public import pool
class tt():
    def __init__(self,i):
        #self.test(i)
        print i
    # def test(self,i):
    #     # conn=mysqlpool(i)
    #
    #
    #     conn = pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
    #     cur=conn.cursor()
    #     SQL="select * from users"
    #     r=cur.execute(SQL)
    #     r=cur.fetchall()
    #     print i
    #     #print r
    #     cur.close()
    #     conn.close()