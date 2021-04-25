# -*- coding: utf-8 -*-
import os
def gpuinfo():
	gpus=os.popen('nvidia-smi')
	infos=gpus.read().splitlines()
	ls=[]
	for i in infos:
		e=i.find("MiB")
		if e!=-1:
			ls.append(i)
	if len(ls)==0:
		ls.append("这机子八成没装Nvidia驱动或者没装CUDA")
	return ls

if __name__ == '__main__':
	a=gpuinfo()
	print(a)
