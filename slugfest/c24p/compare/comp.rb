
as = {}
bs = {}
a = []
File.open('log').readlines.each {
	|l| n = l.scan(/\d+/)
	b = []
	n.each {|q| b<<q.to_i}
	b.sort!()
	
	k = b.join('_')

	if not as[k]
		as[k] = []
	end 
	as[k] << l
}


File.open('logs.txt').readlines.each {
	|l| n = l.split(' ')
	d = n[4,10]
	b = []
	d.each {|q| b<<q.to_i}
	b.sort!()
	
	k = b.join('_')

	if not bs[k]
		bs[k] = []
	end 
	bs[k] << l
}


count = 0
as.each{|a, b|  
	if  bs[a].size != b.size 
	puts b, bs[a],"-----\n"; count+=bs[a].size-b.size  
	end
}
p count