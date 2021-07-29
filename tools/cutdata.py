# -*- coding: utf-8 -*-
# 数据集分割工具
import pandas as pd
import os
import glob
import random
import shutil

print("1.生成数据集分割文件")
print("2.根据分割文件生成数据集")
print("3.直接划分数据集")

num=input("输入选项:")

def getfilename(file):
	return os.path.split(file)[1]

def makefile(folder,trainp):
	folder=folder.replace("\\","/")
	folder=folder.replace("\"","")
	files=glob.glob(folder+"/*.*")
	random.shuffle(files)
	if trainp == "":
		trainp=0.9
	else:
		trainp=float(trainp)
	trainnum=int(len(files)*trainp)
	txt=""
	for i in range(trainnum):
		filename=getfilename(files[i])
		txt+=(filename+","+"train\n")
	for i in range(trainnum,len(files)):
		filename=getfilename(files[i])
		txt+=(filename+","+"test\n")
	with open("train.csv",'w',encoding='utf-8') as f:
		f.write("filename,mode\n")
		f.write(txt)
	print("划分完毕！")

def makedatasetbyfile(folder,file):
	folder=folder.replace("\\","/")
	folder=folder.replace("\"","")
	file=file.replace("\\","/")
	file=file.replace("\"","")
	os.mkdir(folder+"/train")
	os.mkdir(folder+"/test")
	csv=pd.read_csv(file)
	for i in range(len(csv)):
		filename=csv.ix[i,"filename"]
		mode=csv.ix[i,"mode"]
		if mode == "train":
			shutil.move(folder+f"/{filename}",f"{folder}/train/{filename}")
		else:
			shutil.move(folder+f"/{filename}",f"{folder}/test/{filename}")
	print("分割完毕！")


if num=="1":
	folder=input("输入作为参考的文件夹:\n")
	trainp=input("输入训练集百分比(默认为0.9):")
	makefile(folder,trainp)
elif num=="2":
	folder=input("输入要分割的文件夹:\n")
	cutfile=input("输入分割文件:\n")
	makedatasetbyfile(folder,cutfile)
elif num=="3":
	folder=input("输入要分割的文件夹:\n")
	trainp=input("输入训练集百分比(默认为0.9):")
	makefile(folder,trainp)
	makedatasetbyfile(folder,"train.csv")


# data=pd.read_csv("8.csv")
# print(len(data))