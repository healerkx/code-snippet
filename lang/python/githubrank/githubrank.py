#encoding=utf-8

import sys
from pyquery import PyQuery as pq
import codecs

c = 0
d = pq(url = 'http://githubrank.com')
table = d('table')
lines = []
for j in pq(table).find('tr'):
	a = pq(j).find('td')
	if len(a) <= 2:
		continue
	order = pq(a[0]).text()
	href = pq(a[2]).find('a').attr('href')
	name = pq(a[2]).find('a').text()
	addr = pq(a[4]).text()
	skill = pq(a[5]).text()
	#print skill
	line = '|'.join([order, name, href, addr, skill])
	lines.append(line)

print a[0]
#exit()

f = codecs.open("d:\\url.txt", "w", "utf-8")
for i in lines:
	f.write(i)
	f.write("\n")
f.close()
	
