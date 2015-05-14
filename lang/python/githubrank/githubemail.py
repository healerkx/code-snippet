#encoding=utf-8

import sys
from pyquery import PyQuery as pq
import codecs


f = codecs.open("d:\\url.txt", "r", "utf-8")
lines = f.readlines()
f2 = codecs.open("d:\\url2.html", "w", "utf-8")
f2.write("<table>")
c = 0
for line in lines:
	#print line
	i = line.split("|")
	d = pq(url = i[2])
	email = d.find("a.email").text()
	#email = "a@b.c"
	i.append(email)

	style='#FFCCCC'
	if c % 2 == 0:
		style='#99CC00'
	td = "</td><td style='background:%s'>" % style
	line = td.join(i)
	f2.write("<tr><td>")
	f2.write(line)
	f2.write("</td></tr>")
	f2.write("\n")
	c += 1
	print c

f2.write("</table>")
f.close()
f2.close()
	