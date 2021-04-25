# -*- coding: UTF-8 -*-
import numpy as np
import io
import tarfile
from io import  BytesIO
from PIL import Image
import pickle

class TarFileReader(object):
    """本库将Tar文件作为二进制数据集使用，需要配合一个pkl标签文件合作更佳"""
    def __init__(self, filename,filters=None):
        """
            filename:tar文件路径
            filter:一个list，比如[".jpg",".png","txt"]，文件名必须包含这些内容时才会被保留，tar里有目录时此项很有效
            tar中存储的文件名为 目录/目录/../文件名
        """
        super(TarFileReader, self).__init__()
        self.fp=tarfile.open(filename)
        self.content=[]
        if filters!=None:
            for i in self.fp.getmembers():
                for j in filters:
                    if i.name.find(j)!=-1:
                        self.content.append(i)
        else:
            self.content=self.fp.getmembers()
        self.lens=(len(self.content))
    def __len__(self):
        return self.lens
    def getFilebyname(self,name):
        for i in self.content:
            if name == i.name:
                return self.fp.extractfile(i).read()
    def getFilebyIdx(self,idx):
        if(idx>=len(self)):
            return self.fp.extractfile(self.content[0]).read()
        return self.fp.extractfile(self.content[idx]).read()
    def getPILbyName(self,name):
        """
           用图片名获取PIL格式图片
        """
        img=self.getFilebyname(name)
        return Image.open(BytesIO(img))
    def getPILbyIdx(self,idx):
        """
           用index获取PIL格式图片 
        """
        img=self.getFilebyIdx(idx)
        return Image.open(BytesIO(img))
    def getFPbyName(self,name):
        """
           用文件名获取文件指针，主要是给Pickel或者Joblib用 
        """
        for i in self.content:
            if name == i.name:
                return self.fp.extractfile(i)
    def getFPbyIdx(self,idx):
        """
           用index获取文件指针，主要是给Pickel或者Joblib用 
        """
        if(idx>=len(self)):
            return self.fp.extractfile(self.content[0]).read()
    def getPickelbyName(self,name):
        """
           用文件名获取tar里的pickle文件 
        """
        file=getFPbyName(name)
        return pickle.load(file)
    def getPickelbyIdx(self,idx):
        """
           用index获取tar里的pickle文件 
        """
        file=getFPbyIdx(idx)
        return pickle.load(file)

    def getPILbyNameWithName(self,name):
        """
           用图片名获取PIL格式图片
        """
        img=self.getFilebyname(name)
        return Image.open(BytesIO(img)),name
    def getPILbyIdxWithName(self,idx):
        """
           用index获取PIL格式图片 
        """
        img=self.getFilebyIdx(idx)
        name=""
        if(idx>=len(self)):
            name=self.content[0].name
        else:
        	name=self.content[idx].name
        return Image.open(BytesIO(img)),name

    def __del__(self):
        self.fp.close()


if __name__ == '__main__':
    a=TarFileReader("training_set.tar",["jpg"])
    f=a.getPILbyIdxWithName(0)
    f[0].show()