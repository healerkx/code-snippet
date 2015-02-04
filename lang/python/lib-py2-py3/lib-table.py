#encoding=utf-8

import sys
from pyquery import PyQuery as pq


d = pq(url = 'https://www.pythonanywhere.com/batteries_included/')
# d = pq(url = 'd:\\a.html')

n = ['python2.6', 'python2.7', 'python3.3', 'python3.4']
c = 0
r = {}
for i in d('table'):
	a = []
	for j in pq(i).find('tr'):
		#print dir(j.find('td'))
		a.append(pq(j).find('td a').text())

	r[n[c]] = a
	c += 1

l = r[n[0]] + r[n[1]] + r[n[2]] + r[n[3]]
l = sorted(list(set(l)))


f = open('o.html', 'w')
f.write("<table  cellPadding=1 width=800 align=center border=1>")
f.write('<tr><td>Library</td><td>Python 2.6</td><td>Python 2.7</td><td>Python 3.3</td><td>Python 3.4</td></tr>')
for i in l:
	f.write('<tr>')
	f.write("<td>" + i + "</td>")
	for j in range(0, 4):
		try:
			if r[n[j]].index(i) >= 0:
				f.write("<td>%s</td>" % 'Yes')
		except:
			f.write("<td>%s</td>" % 'No')
	f.write('</tr>')
f.write('</table>')	

