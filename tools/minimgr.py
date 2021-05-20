# -*- coding: utf-8 -*-
# 最新版模型自动管理工具
# 相比较前版本的死板,本版本属于开放式管理。更类似于torch.save的延伸版本
# 提供了几个隐藏函数以便扩展本类
import numpy as np
import torch
import os
import datetime

#一个增强的epoch管理工具
#使用方法：
#	ep=epochmgr(20)
#	for i in ep.epoch():
#		...
class epochmgr(object):
	"""docstring for epochs"""
	def __init__(self,maxnum=9999999,minnum=0):
		super(epochmgr, self).__init__()
		self.maxnum=maxnum
		self.minnum=minnum
	def setMax(self,num):
		self.maxnum=num
	def setMin(self,num):
		self.minnum=num
	def epoch(self):
		return range(self.minnum,self.maxnum)

#_dic_maker[注册函数],
#_save[快速保存],
#_dicname[获取注册名],
#_update[更新函数存储空间] 四个函数负责快速扩展minimgr类
#
class minimgr(object):
	"""docstring for minimgr
	本类只是torch.save的封装。最好每个pth/pkl文件对应一个minimgr类。
	mgrname是给每个minimgr类起个名字，好辨别
	"""
	def __init__(self,mgrname):
		super(minimgr, self).__init__()
		self.mgrname= mgrname
		#计数器
		self.num={}
		#存储score等等判定标准
		self.cache={}
		#要save的内容
		self.content={}
		#是否更新
		self.update={}

	def __str__(self):
		return("This is {} management.".format(self.mgrname))

	#load没有任何特殊内容。纯粹为了整齐而编写。只是做了一个判定操作
	def load(self,filename):
		file=None
		if os.path.exists(filename):
			file=torch.load(filename)
		return file

	#为了扩展minimgr方便所设计的函数之一，实现的是best_save最前面一坨初始化用的if
	#如果score是None，说明不存在比较，全部保存。所以这类函数不新建score这个参数
	#func_name:best_save
	#save_name:1
	#全名：best_save_1
	#制作dic时，如果需要类似于append的功能，可以直接在content参数输入 [content]
	def _dic_maker(self,func_name,save_name,content,score=None):
		if ("{}_{}".format(func_name,save_name) in self.num) == False:
			self.num["{}_{}".format(func_name,save_name)]=0
		if ("{}_{}".format(func_name,save_name) in self.cache) == False and score!=None:
			self.cache["{}_{}".format(func_name,save_name)]=score
		if ("{}_{}".format(func_name,save_name) in self.update) == False and score!=None:
			self.update["{}_{}".format(func_name,save_name)]=True
		if ("{}_{}".format(func_name,save_name) in self.content) == False:
			self.content["{}_{}".format(func_name,save_name)]=content
			# print(self.content["{}_{}".format(func_name,save_name)])

	#为了扩展minimgr方便所设计的函数之一，实现的是best_save最后面的保存任务
	#num=0时就是次次保存，score=False时，就无视flag直接保存
	#content不为none时，将输入的content进行保存。此目的是每隔num次才会在内存保存一次
	#不用每次都复制给内存
	#支持mode,content不是None时，mode起作用
	def _save(self,func_name,save_name,filename,num,score=False,content=None,mode="update"):
		self.num["{}_{}".format(func_name,save_name)]+=1
		saveflag=""
		if self.num["{}_{}".format(func_name,save_name)]>=num:
			if content!=None:
				self._contentmode(func_name,save_name,content,mode)
			if score==True:
				if self.update["{}_{}".format(func_name,save_name)]:
					torch.save(self.content["{}_{}".format(func_name,save_name)],filename)
					self.update["{}_{}".format(func_name,save_name)]=False
				else:
					saveflag="not"
			else:
				torch.save(self.content["{}_{}".format(func_name,save_name)],filename)
			self.num["{}_{}".format(func_name,save_name)]=0
			return("{}_{}: may{} save at {}".format(func_name,save_name,saveflag,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
			# print("{}_{}: has saved at {}".format(func_name,save_name,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		else:
			return ""
	#为了扩展minimgr方便所设计的函数之一，实现的是返回当前save对应的字典真实名字
	def _dicname(self,func_name,save_name):
		return "{}_{}".format(func_name,save_name)

	#一个简化update函数。省去best_save中间的update部分.本函数会直接根据mode更新数据
	#不会管大于小于等问题,可以理解为强制更新
	#mode
	#	update:直接更新
	#	append:向后添加
	#	add:累加
	def _update(self,func_name,save_name,content,score=None,mode="update"):
		if score!=None:
			self.cache["{}_{}".format(func_name,save_name)]=score
			self.update["{}_{}".format(func_name,save_name)]=True
		self._contentmode(func_name,save_name,content,mode)

	#	update:直接更新
	#	append:向后添加
	#	add:累加
	#	本函数具体用法参看_update以及_save方法
	def _contentmode(self,func_name,save_name,content,mode="update"):
		if mode=="update":
			self.content["{}_{}".format(func_name,save_name)]=content
		elif mode=="append":
			# print(self.content["{}_{}".format(func_name,save_name)])
			self.content["{}_{}".format(func_name,save_name)].append(content)

	#取最好的score进行缓存。调用本函数num次后持久化一次。mode有 min,max ...诸多模式。
	#为min时,选取前面最小的值保存。threshold是一个阈值。如果score<最小值-threshold，才会认为更小
	#此处的score是一个标量
	#name是为了偷懒做的。给每个save起个名字，就可以使用minimgr类保存不同的文件
	def best_save(self,score,content,filename,mode="min",threshold=1e-10,num=5,name="1"):
		if ("best_save_{}".format(name) in self.num) == False:
			self.num["best_save_{}".format(name)]=0
		if ("best_save_{}".format(name) in self.cache) == False:
			self.cache["best_save_{}".format(name)]=score
		if ("best_save_{}".format(name) in self.update) == False:
			self.update["best_save_{}".format(name)]=True
		if ("best_save_{}".format(name) in self.content) == False:
			self.content["best_save_{}".format(name)]=content
		saveflag=""
		if mode=="min":
			if score<self.cache["best_save_{}".format(name)]-threshold:
				self.cache["best_save_{}".format(name)]=score
				self.content["best_save_{}".format(name)]=content
				self.update["best_save_{}".format(name)]=True
		if mode=="max":
			if score>self.cache["best_save_{}".format(name)]+threshold:
				self.cache["best_save_{}".format(name)]=score
				self.content["best_save_{}".format(name)]=content
				self.update["best_save_{}".format(name)]=True
						
		self.num["best_save_{}".format(name)]+=1
		if self.num["best_save_{}".format(name)]>=num:
			if self.update["best_save_{}".format(name)]:
				torch.save(self.content["best_save_{}".format(name)],filename)
				self.update["best_save_{}".format(name)]=False
			else:
				saveflag="not"
			self.num["best_save_{}".format(name)]=0
			return("best_save_{}: may{} save at {}".format(name,saveflag,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		else:
			return ""

	#除了第一个值自动保存，剩下的使用lambda_func来判定是否缓存此值。调用本函数num次后持久化一次。lambda_func具有两个参数，分别是
	# 现在的score,以及之前最后一次缓存的值。此处的score可以是lambda_func可以处理的任意量
	# lambda_func返回一个布尔值，参数是 lambda_func(新score,旧score)
	def lambda_save(self,score,content,filename,lambda_func,num=5,name="1"):
		if ("lambda_save_{}".format(name) in self.num) == False:
			self.num["lambda_save_{}".format(name)]=0
		if ("lambda_save_{}".format(name) in self.cache) == False:
			self.cache["lambda_save_{}".format(name)]=score
		if ("lambda_save_{}".format(name) in self.update) == False:
			self.update["lambda_save_{}".format(name)]=True
		if ("lambda_save_{}".format(name) in self.content) == False:
			self.content["lambda_save_{}".format(name)]=content
		saveflag=""
		if lambda_func(score,self.cache["lambda_save_{}".format(name)]):
			self.update["lambda_save_{}".format(name)]=True
			self.cache["lambda_save_{}".format(name)]=score
			self.content["lambda_save_{}".format(name)]=content


		self.num["lambda_save_{}".format(name)]+=1
		if self.num["lambda_save_{}".format(name)]>=num:
			if self.update["lambda_save_{}".format(name)]:
				torch.save(self.content["lambda_save_{}".format(name)],filename)
				self.update["lambda_save_{}".format(name)]=False
			else:
				saveflag="not"
			self.num["lambda_save_{}".format(name)]=0
			return("lambda_save_{}: may{} save at {}".format(name,saveflag,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		else:
			return ""


	#每隔num次,直接保存,保存的内容就是第num次的内容
	def step_save(self,content,filename,num=5,name="1"):
		self._dic_maker("step_save",name,content,score=None)
		return self._save("step_save",name,filename,num,score=False,content=content)
		
	
	#将前面所有内容缓存进入一个列表，每隔num个间隔持久化一次。但是会存储之前的所有内容。适合用于保存曲线
	#之类的内容
	def cache_save(self,content,filename,num=5,name="1"):
		self._dic_maker("cache_save",name,[],score=None)
		self._update("cache_save",name,content,mode="append")
		return self._save("cache_save",name,filename,num,score=False,mode="append")

	#此处返回布尔值，每隔num次返回一个bool,用以做计数器
	def counter(self,num=5,name="1"):
		self._dic_maker("counter",name,0,score=None)
		self.num[self._dicname("counter",name)]+=1
		if self.num[self._dicname("counter",name)]>=num:
			self.num[self._dicname("counter",name)]=0
			return True

if __name__ == '__main__':
	import time
	mi=minimgr("tester")
	epoch=epochmgr(20)
	for i in epoch.epoch():
		if mi.counter(8):
			print("又八次")