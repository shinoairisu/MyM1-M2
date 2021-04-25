# -*- coding: utf-8 -*-
import requests
def reader():
	ips=[]
	with open(r'ip.txt','r',encoding='utf-8') as f:
		e=f.read().splitlines()
		for i in e:
			if i!="":
				ips.append(i)
	return ips

def getter():
	e=""
	ips=reader()
	for i in ips:
		f=""
		try:
			f=requests.get(f'http://{i}/gpu')
			f=f.text
		except:
			f="这机子联系不上，下一个！"
		if i.find(":")==-1:
			i=i
		else:
			i=i[:i.find(":")]
		text="<h1>"+i+"的信息</h1>"+ f
		e=e+text
	return e

if __name__ == '__main__':
	print(reader())