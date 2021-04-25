# -*- coding: utf-8 -*-
# Lossholder v1.0
# 使用本库必须安装Pytorch
# 本库有几个能力：
# 1.执行n回管理函数后的模型自动保存
# 2.保存test_loss最低点或者acc最高数据，或者都保存
import torch
import pickle
import os

#托管的批处理管理器
class Epocher(object):
	"""docstring for Epocher"""
	def __init__(self,min=0 ,max=20):
		super(Epocher, self).__init__()
		self.arg = arg

class LossHolder(object):
	"""通过loss来管理model数据的库
	   scheduler是自动学习率管理器，为None说明没有
	"""
	def __init__(self, model, optimizer,epocher,scheduler=None):
		"""
			本类会自动定时保存模型
			注意输入的loss和acc一般是testacc和testloss
			未测试，可能有bug
		"""
		super(LossHolder, self).__init__()
		self.model = model
		self.epochcount=20
		self.mode=mode
		self.loss=None
		self.lossdic=[]
		self.accdic=[]
		self.acc=None
		self.epoch=0
	def losshandle(self,loss):
		if self.loss=None:
			if loss<1000000:
				self.loss=loss
				self.lossdic=self.model.state_dict()
		else
			if loss<self.loss:
				self.loss=loss
				self.lossdic=self.model.state_dict()

	def acchandle(self,acc):
		if self.acc=None:
			if acc>0:
				self.acc=acc
				self.accdic=self.model.state_dict()
		else
			if acc>self.acc:
				self.acc=acc
				self.accdic=self.model.state_dict()
	
	def lossacchandle(self,loss,acc):
		self.losshandle(loss)
		self.acchandle(acc)

	def autosave(self,epochcount=20):
		self.epoch+=1
		if self.epoch==epochcount:
			self.saver()
			self.epoch=0
	def saver(self):
		dicer={}
		dicer["loss"]=None
		dicer["acc"]=None
		if self.acc!=None:
			torch.save(self.accdic,"acc_best.pkl")
			dicer["acc"]=self.acc
			print("======*****acc_best.pkl has saved*****======")
		if self.loss!=None:
			torch.save(self.lossdic,"loss_min.pkl")
			dicer["loss"]=self.loss
			print("======*****loss_min.pkl has saved*****======")
		torch.save(self.model.state_dict(),"now_model.pkl")
		print("======*****now_model.pkl has saved*****======")
		fp=open('pram.pkl','wb')
		pickle.dump(fp,dicer)
		fp.close()
	


	def lossAndsave(self,loss,epochcount=20):
		"""
			时刻保存最低的test_loss模型
			并每隔一定训练批次保存模型
			epochcount，指调用本函数epochcount次后，会自动保存模型数据
		"""
		self.losshandle(loss)
		self.autosave(epochcount)
	def accAndsave(self,acc,epochcount=20):
		"""
			时刻保存最高的test_acc模型
			并每隔一定训练批次保存模型
			epochcount，指调用本函数epochcount次后，会自动保存模型数据
		"""
		self.acchandle(acc)
		self.autosave(epochcount)
	def acclossAndsave(self,loss,acc,epochcount=20):
		"""
			时刻保存最高的test_acc与最低的test_loss模型
			并每隔一定训练批次保存模型
			epochcount，指调用本函数epochcount次后，会自动保存模型数据
		"""
		self.lossacchandle(loss,acc)
		self.autosave(epochcount)

	def saverOnlyNow(self,epochcount=20):
		"""
			与前面方法不同，本函数只定期保存当前训练结果
		"""
		self.epoch+=1
		if self.epoch==epochcount:
			torch.save(self.model.state_dict(),"now_model.pkl")
			self.epoch=0
		


	def loadModel(self,mode="now",path=""):
		"""
			读取模型
			如果当前目录下有模型，会自动将模型读取进网络
			mode参数:
				now:读取当前目录下now_model.pkl
				path:读取指定路径的模型
		"""
		if mode=="now":
			if os.path.exists("now_model.pkl"):
				dic=torch.load("now_model.pkl")
				self.model.load_state_dict(dic)
				print(f"Loaded now_model.pkl")
			else:
				print("Can't find now_model.pkl")
		else:
			if path!="" and os.path.exists(path):
				dic=torch.load(path)
				self.model.load_state_dict(dic)
				print(f"Loaded {path}")
			else:
				print(f"Can't find {path}")
		dix=None
		if os.path.exists("pram.pkl"):
			fp=open('pram.pkl','wb')
			dix=pickle.load(fp)
			fp.close()
			print(f"Loaded pram.pkl")
		if dix!=None:
			if dix["loss"]!=None:
				if os.path.exists("loss_min.pkl"):
					self.loss=dix["loss"]
					self.lossdic=torch.load("loss_min.pkl")
					print(f"Loaded loss_min.pkl")
			if dix["acc"]!=None:
				if os.path.exists("acc_best.pkl"):
					self.acc=dix["acc"]
					self.accdic=torch.load("acc_best.pkl")
					print(f"Loaded acc_best.pkl")



			