# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:03:42 2017
@author: lenovo
F:/HeadFirst/Naive Bayes/docclass.py
Chapter6 Naive Bayes
"""

import re
import math

def sampletrain(c1):
    #简单的训练样本
    c1.train('Nobody owns the water','good')
    c1.train('the quick rabbit jumps fences','good')
    c1.train('buy pharmaceuticals now','bad')
    c1.train('make quick money at the online casino','bad')
    c1.train('the quick brown fox jumps','good')

def getwords(doc):
    #函数功能：特征提取
    #将参数doc文本(str)拆分为单词，拆分规则为任何非字母类字符
    splitter = re.compile('\\W*')
    #根据非字母字符进行单词拆分
    words = [s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    
    #只返回一组不重复的单词
    return dict([(w,1) for w in words])

class classifier:
    def __init__(self,getfeatures=getwords,filename=None):
        #统计特征/分类组合的数量
        #各分类中不同特征的数量
        #{'python':{'bad':0,'good':0},'the':{'bad':3,'good':0}}
        self.fc = {}
        #统计每个分类中的文档数量
        self.cc = {}
        #对应一个函数：从即将被归类的内容项提取特征
        self.getfeatures = getfeatures
        
        
    def incf(self,f,cat):
        #增加对特征/分类组合的计数值
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat] += 1
               
    def incc(self,cat):
        #增加对某一分类的计数值
        self.cc.setdefault(cat,0)
        self.cc[cat] += 1
    
    def fcount(self,f,cat):
        #某一特征出现于某一分类的次数
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    
    def catcount(self,cat):
        #属于某一分类的内容项数量
        if cat in self.cc:
            return float(self.cc[cat])
        return 0
    
    def totalcount(self):
        #所有内容项数量
        return sum(self.cc.values())
    
    def categories(self):
        #所有分类列表
        return self.cc.keys()
    
    def train(self,item,cat):
        #item:内容项（文档）；cat:分类
        features = self.getfeatures(item)
        #针对分类为每个特征增加计数值
        for f in features:
            self.incf(f,cat)
        
        #增加针对该分类的计数值
        self.incc(cat)
        
    def fprob(self,f,cat):
        if self.catcount(cat) == 0:
            return 0
        #特征在分类中出现的总次数，除以分类中包含内容项的总数
        return self.fcount(f,cat)/self.catcount(cat)
    
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        #ap = 假设概率，weight = 假设概率的权重
        basicprob = prf(f,cat)
        #统计特征在所有分类中出现的次数
        totals = sum([self.fcount(f,c) for c in self.categories()])
        #计算加权平均
        bp = ((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp  
      
class fisherclassifier(classifier):
    def __init__(self,getfeatures=getwords):
        classifier.__init__(self,getfeatures)
        #保存临界值
        self.minimums={}
        
    def setminimum(self,cat,minn):
        self.minimums[cat] = minn
                     
    def getminimum(self,cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]
    
    def cprob(self,f,cat):
        #Pr(category\feature)
        #特征在该分类中出现的概率
        clf = self.fprob(f,cat)
        if clf == 0: return 0
        #特征在所有分类中出现的概率
        freqsum = sum([self.fprob(f,c) for c in self.categories()])
        p = clf/freqsum
        return p

    def fisherprob(self,item,cat):
        #所有概率值相乘
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*= (self.weightedprob(f,cat,self.cprob))
        #取自然对数并乘以-2  
        fscore = -2*math.log(p)
        #利用倒置对数卡方函数求得概率
        return self.invchi2(fscore,len(features)*2)
    
    def invchi2(self,chi,df):
        m = chi/2.0
        summ = term = math.exp(-m)
        for i in range(1, df//2):
            term*= m/i
            summ+=term
        return min(summ,1.0)
    
    def classify(self,item,default=None):
        #循环遍历并寻找最佳结果
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item,c)
            #确保其超过下限值
            if p>self.getminimum(c) and p>max:
                best = c
                max = p
            return best
        
class naivebayes(classifier):
    def __init__(self,getfeatures=getwords):
        classifier.__init__(self,getfeatures)
        #定义阈值
        self.thresholds = {}
        
    def setthreshold(self,cat,t):
        self.thresholds[cat] = t
                       
    def getthreshold(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]
    
    def docprob(self,item,cat):
        #Pr(Document|Category)
        features = self.getfeatures(item)
        
        #将所有特征的概率相乘
        p = 1
        for f in features:
            p *= self.weightedprob(f,cat,self.fprob)
        return p
    def prob(self,item,cat):
        #Pr(Category)
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item,cat)
        #Pr(Document|Category)*Pr(Category)
        return docprob * catprob
    
    def classify(self,item,default=None):
        probs = {}
        #寻找概率最大的分类
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item,cat)
            if probs[cat]>max:
                max = probs[cat]
                best = cat
        #确保概率值大于域值*次大概率      
        for cat in probs:
            if cat == best:continue
            if probs[cat]*self.getthreshold(best)>probs[best]:
                return default
            
        return best
    

        


















































































































