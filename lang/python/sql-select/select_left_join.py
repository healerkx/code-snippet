# -*- coding: UTF8 -*-

import MySQLdb
import time

c = MySQLdb.Connect(host = '127.0.0.1', user = 'root', passwd = '123', db = 'xjy_main')
cur = c.cursor()

try:
    b = time.time()
    cur.execute("select * from xjy_friend f left join xjy_user u on f.user_id=u.user_id where f.friend_user_id=17 or f.friend_user_id=18")
    for row in cur.fetchall():
    	pass
    print time.time() - b
except Exception as e:
    print(e)
finally:
    pass
