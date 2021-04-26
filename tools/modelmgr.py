# -*- coding: utf-8 -*-
# 新版模型自动管理工具
import numpy as np
import torch
import os

#一个增强的epoch管理工具,可以交给netmgr进行管理
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
		return range(minnum,maxnum)		

#神经网络管理器，负责定时保存网络数据，启动时自动加载数据继续训练
#使用方法：
#a=netmgr()
#a.setModel(...)
#a.AutoLoad(...)
#...
#for i in epoch:
#	...
#	a.step()
class netmgr(object):
	"""model是模型
		opt是优化器
		epoch是增强的epoch管理工具
	"""
	def __init__(self):
		super(netmgr, self).__init__()
		self.dic = {}
		self.dic["acc"]=None #存储最优acc的网络参数
		self.dic["best_acc"]=0 #存储最优acc值
		self.dic["loss"]=None #存储最优loss的网络参数
		self.dic["best_loss"]=9999999#存储最优的loss数值
		self.dic["now_Net"]=None #存储当前网络参数
		self.dic["opt"]=None #存储当前优化器参数
		self.dic["epoch"]=None #存储进行到的epoch数
		self.dic2={} #存储曲线
		self.dic2["train_acc"]=[] #存储之前的acc曲线
		self.dic2["train_loss"]=[] #存储之前的loss曲线
		self.dic2["eval_acc"]=[]
		self.dic2["eval_loss"]=[]
		self.model=None
		self.opt=None
		self.epochmgr=None
		self.scheduler=None
		self.acc=False
		self.loss=False
		self.curve=True
		self.modelname=""
		self.count=0

	def setModel(self,model,opt,epochmgr,scheduler=None,acc=False,loss=False,curve=True,modelname="model"):
		#新版的netmgr不在依赖构造函数，而是可以动态设置管理内容
		#这个函数必须在AutoLoad之前
		#epoch不是epoch
		#acc指保存acc最大模型，loss指保存loss最小模型
		#acc,loss是指保存最优acc模型，以及最优loss模型，now是必选,curve可选但是默认是打开的
		#opt是优化器
		#scheduler 这是学习率自动管理器,允许为空
		self.model=model
		self.opt=opt
		self.epochmgr=epochmgr
		self.acc=acc
		self.loss=loss
		self.curve=curve
		self.modelname=modelname

	def setAutoLoad(self,load=False,modepath="./"):
		#此函数自动查看目录下的文件，如果有自动加载到程序中。load设置为false就是关闭了AutoLoad功能，每次都是新训练
		#modepath填写的是一个目录，不是文件！比如 c://exp/。当前目录就是 ./
		#本程序保管文件格式特殊，所以必须收到一组文件。
		if load!=False:
			path_model=os.path.join(modepath,"{}.pt".format(self.modelname))
			path_curve=os.path.join(modepath,"{}_Curve.pt".format(self.modelname))
			if os.path.exists(path_model):
				self.dic=torch.load(path_model)
				self.model.load_state_dict(self.dic["now_Net"])
				self.opt.load_state_dict(self.dic["opt"])
				if scheduler!=None:
					scheduler.last_epoch=self.dic["epoch"]
				self.epochmgr.setMin(self.dic["epoch"])
			if os.path.exists(path_curve) and self.curve:
				self.dic2=torch.load(path_curve)

	def _save(self):
		self.dic["now_Net"]=self.model.state_dict()
		self.dic["opt"]=self.opt.state_dict()
		torch.save(self.dic,"{}.pt".format(self.modelname))
		print("The {}.pt has saved at {} epoch".format(self.modelname,self.dic["epoch"]))
		if self.curve==True:
			torch.save(self.dic,"{}_Curve.pt".format(self.modelname))
			print("The {}_Curve.pt has saved at {} epoch".format(self.modelname,self.dic["epoch"]))

	#这个函数用于内存设置字典
	def _setter(self,test_acc=-1,test_loss=-1,acc_threshold=1e-4,loss_threshold=1e-4):
		if self.acc==True:
			if test_acc>self.dic["best_acc"]+acc_threshold:
				self.dic["best_acc"]=test_acc
				self.dic["acc"]=self.model.state_dict()
		if self.loss==True:
			if test_loss<self.dic["best_loss"]-loss_threshold:
				self.dic["best_loss"]=test_loss
				self.dic["loss"]=self.model.state_dict()

	def _curvesave(self,evacc,evloss,tacc,tloss):
		if evacc>-1:
			self.dic2["eval_acc"].append(evacc)
		if evloss>-1:
			self.dic2["eval_loss"].append(evloss)
		if tacc>-1:
			self.dic2["train_acc"].append(tacc)
		if tloss>-1:
			self.dic2["train_loss"].append(tloss)

	def getCurve(self,filepath):
		#单独使用这个函数可以直接读取某个Curve文件
		return torch.load(filepath)


	def step(self,num=5,epoch,test_acc=-1,acc_threshold=1e-4,test_loss=-1,loss_threshold=1e-4,train_acc=-1,train_loss=-1):
		#此函数是设置几个回合后存储数据,但是内存是每个回合都会存储的
		"""num 指几个epoch后存储
		acc是testacc，loss是testloss
		threshold是指,向指定方向变动大于这个数值时才存储。减少内存变动。比如这次acc=85,下次必须大于85+1e-4才存储，否则认为是一样大的。
		本函数除了
		"""
		self._curvesave(test_acc,test_loss,train_acc,train_loss)
		self._setter(test_acc,test_loss,acc_threshold,loss_threshold)
		self.dic["epoch"]=epoch
		self.count+=1
		if self.count>=num:
			self._save()
			self.count=0
		



