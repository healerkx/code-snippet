# -*- coding: UTF8 -*- 

import MySQLdb
import time

c = MySQLdb.Connect(host = '127.0.0.1', user = 'root', passwd = '123', db = 'xjy_main')
cur = c.cursor()

try:
    b = time.time()
    cur.execute("select * from xjy_user where user_id in (select distinct user_id from xjy_friend where friend_user_id=17 or friend_user_id=18)")

    print time.time() - b
except Exception as e:
    print(e)
finally:
    pass
