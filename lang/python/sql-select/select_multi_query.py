# -*- coding: UTF8 -*- 

import MySQLdb
import time

c = MySQLdb.Connect(host = '127.0.0.1', user = 'root', passwd = '123', db = 'xjy_main')
cur = c.cursor()

try:
    b = time.time()
    cur.execute("select distinct user_id from xjy_friend where friend_user_id=17 or friend_user_id=18")
    user_id_list = []
    for row in cur.fetchall():
    	user_id = row[0]
    	user_id_list.append(str(user_id))
    # print user_id_list
    id_list = ','.join(user_id_list)
  
    cur.execute("select user_id from xjy_user where user_id in (%s)" % id_list)
    print time.time() - b
except Exception as e:
    print(e)
finally:
    pass
