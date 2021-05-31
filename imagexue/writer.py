# -*- coding: utf-8 -*-
import os
import random
import math
"""
	制作一个漫反射球
	position 位置
	r 半径
	color 颜色
	ks:镜面反射系数 小于1
	b:镜面反射指数 大于1的整数
"""
def makeBall_opaq(outmap=[],position=[0.,0.,0.],r=5.,color=[255,0,0],ks=0.6,b=10):
	color1=0.0
	color2=0.0
	color3=0.3
	if color!="random":
		color1=color[0]/255.0*1.0
		color2=color[1]/255.0*1.0
		color3=color[2]/255.0*1.0
	else:
		color1=random.randint(0,255)/255.0*1.0
		color2=random.randint(0,255)/255.0*1.0
		color3=random.randint(0,255)/255.0*1.0
	outmap.append(f"sphe	{position[0]}  {position[1]}  {position[2]} {r}")
	outmap.append(f"opaq	{round(color1,2)}  {round(color2,2)}  {round(color3,2)}  {ks}  {b}")
	return outmap

"""
	制作一个镜面球
	position 位置
	r 半径
"""
def makeBall_mirror(outmap=[],position=[0.,0.,0.],r=5.):
	outmap.append(f"sphe	{position[0]}  {position[1]}  {position[2]} {r}")
	outmap.append(f"mirr")
	return outmap

"""
	制作一个透明球

	ks:镜面反射系数 小于1
	b:镜面反射指数 大于1的整数
	kt:透明系数 小于1
	n：折射率 大于1的小数
"""
def makeBall_transparent(outmap=[],position=[0.,0.,0.],r=5.,kt=0.8,n=1.5,ks=0.2,b=10):
	outmap.append(f"sphe	{position[0]}  {position[1]}  {position[2]} {r}")
	outmap.append(f"trpa 	{kt}  {n}  {ks}  {b}")
	return outmap

"""
	使用某个球画一条线
	ball:球的类别 op mr tr ran  漫反射 镜面 透明 随机
	from: 起始点
	to: 结束点
	z: 所在平面
	number: 用多少个球来填充线段
	color：球的颜色 可以是一个list，也可以是random。
	ks:镜面反射系数 小于1
	b:镜面反射指数 大于1的整数
	kt:透明系数 小于1
	n：折射率 大于1的小数
	ks=0.6,b=10,kt=0.5,n=1.5

"""
def drawLine(outmap=[],ball="op",fromPoint=[0.,0.],toPoint=[0.,0.],z=0.,number=5,r=5.,color=[255,255,0],ks=0.6,b=10,kt=0.5,n=1.5):
	k=(toPoint[1]-fromPoint[1])/(toPoint[0]-fromPoint[0])
	bs=(fromPoint[0]*toPoint[1]-toPoint[0]*fromPoint[1])/(toPoint[0]-fromPoint[0])
	leng=(toPoint[0]-fromPoint[0])/number
	xs=[]
	ys=[]
	start=fromPoint[0]
	for i in range(number):
		xs.append(start)
		ys.append(k*start+bs)
		start+=leng
	if ball=="op":
		for i in range(number):
			makeBall_opaq(outmap,position=[xs[i],ys[i],z],r=r,color=color,ks=ks,b=b)
			# print(b)
	elif ball=="mr":
		for i in range(number):
			makeBall_mirror(outmap,position=[xs[i],ys[i],z],r=r)
	elif ball=="tr":
		for i in range(number):
			makeBall_transparent(outmap,position=[xs[i],ys[i],z],r=r,kt=kt,n=n,ks=ks,b=b)
	else:
		for i in range(number):
			fx=random.randint(1,10000)
			if fx%3==0:
				makeBall_opaq(outmap,position=[xs[i],ys[i],z],r=r,color=color,ks=ks,b=b)
			elif fx%3==1:
				makeBall_mirror(outmap,position=[xs[i],ys[i],z],r=r)
			elif fx%3==2:
				makeBall_transparent(outmap,position=[xs[i],ys[i],z],r=r,kt=kt,n=n,ks=ks,b=b)
	return outmap



"""
	使用某个球画sin
	factor 是在y轴上波动的扩大
"""
def drawSin(outmap=[],ball="op",fromPoint=[0.,0.],toPoint=[0.,0.],r=5.,z=0,factor=60,number=20,color=[255,255,0],ks=0.6,b=10,kt=0.5,n=1.5):
	leng=(toPoint[0]-fromPoint[0])/number
	xs=[]
	ys=[]
	start=fromPoint[0]
	starty=0
	for i in range(number):
		xs.append(start)
		ys.append(round(math.sin(starty)*factor,2))
		start+=leng
		starty+=leng
	if ball=="op":
		for i in range(number):
			makeBall_opaq(outmap,position=[xs[i],ys[i],z],r=r,color=color,ks=ks,b=b)
			# print(b)
	elif ball=="mr":
		for i in range(number):
			makeBall_mirror(outmap,position=[xs[i],ys[i],z],r=r)
	elif ball=="tr":
		for i in range(number):
			makeBall_transparent(outmap,position=[xs[i],ys[i],z],r=r,kt=kt,n=n,ks=ks,b=b)
	else:
		for i in range(number):
			fx=random.randint(1,10000)
			if fx%3==0:
				makeBall_opaq(outmap,position=[xs[i],ys[i],z],r=r,color=color,ks=ks,b=b)
			elif fx%3==1:
				makeBall_mirror(outmap,position=[xs[i],ys[i],z],r=r)
			elif fx%3==2:
				makeBall_transparent(outmap,position=[xs[i],ys[i],z],r=r,kt=kt,n=n,ks=ks,b=b)
	return outmap



"""
	使用某球画圈
	jiaodu：每隔xx度一个球
	cic_r :画的圈的半径
	r:画的球的半径
"""
def drawCic(outmap=[],ball="op",centerPoint=[0.,0.],cic_r=20.,z=0,r=5.,jiaodu=5,color=[255,255,0],ks=0.6,b=10,kt=0.5,n=1.5):
	a=math.pi/180*jiaodu #弧度
	number=int(360/jiaodu)
	th=0
	xs=[]
	ys=[]
	for i in range(number):
		xs.append(round(centerPoint[0]+cic_r*math.cos(math.pi/180*th),2))
		ys.append(round(centerPoint[1]+cic_r*math.sin(math.pi/180*th),2))
		th+=jiaodu
		# print(ys)
	if ball=="op":
		for i in range(number):
			makeBall_opaq(outmap,position=[xs[i],ys[i],z],r=r,color=color,ks=ks,b=b)
			# print(b)
	elif ball=="mr":
		for i in range(number):
			makeBall_mirror(outmap,position=[xs[i],ys[i],z],r=r)
	elif ball=="tr":
		for i in range(number):
			makeBall_transparent(outmap,position=[xs[i],ys[i],z],r=r,kt=kt,n=n,ks=ks,b=b)
	else:
		for i in range(number):
			fx=random.randint(1,10000)
			if fx%3==0:
				makeBall_opaq(outmap,position=[xs[i],ys[i],z],r=r,color=color,ks=ks,b=b)
			elif fx%3==1:
				makeBall_mirror(outmap,position=[xs[i],ys[i],z],r=r)
			elif fx%3==2:
				makeBall_transparent(outmap,position=[xs[i],ys[i],z],r=r,kt=kt,n=n,ks=ks,b=b)
	return outmap



"""
	最终输出以及合成图像
	bg: 背景色
	size:图像长边大小
	resolution:长短边比例
	picname:输出图片名
	mapname:输出图片指令文件名
"""
def outAndRend(outmap,bg=[255,255,255],size="500",resolution=["50.","50."],picname="test.ppm",mapname="myxx.dat"):
	outmap.append(f"back     {bg[0]}  {bg[1]}  {bg[2]}")
	outmap.append("plig     0.5    0.5     2.   255.   255.   255.")
	outmap.append("elig    0.2")
	outmap.append("eyep    1.   0.    150.")
	outmap.append("refp      0.     0.     0.")
	outmap.append(f"vang     {resolution[0]}    {resolution[1]}")
	outmap.append(f"size     {size}")
	outmap.append(f"rend    {picname}")
	outmap.append("quit")
	with open(mapname, "w", encoding="utf-8") as temp:
		for i in outmap:
			temp.write(i+"\n")
	print("write Done.")
	os.system(f"Raycast.exe {mapname}")