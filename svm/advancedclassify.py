# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:35:17 2017
Support Vector Machine
@author: lenovo
"""
import math

class matchrow:
    def __init__(self,row,allnum=False):
        #allnum参数：所有特征均为数值型
        if allnum:
            self.data=[float(row[i]) for i in range(len(row)-1)]
        else:
            self.data=row[0:len(row)-1]
        self.match = int(row[len(row)-1])
        
def loadmatch(f, allnum=False):
    rows=[]
    for line in file(f):
        rows.append(matchrow(line.split(','),allnum))
    return rows

def lineartrain(rows):
    #计算数值型特征分类的均值点
    averages =  {}
    counts = {}
    
    for row in rows:
        #得到该坐标点所属的分类
        c1 = row.match
        
        averages.setdefault(c1,[0.0]*(len(row.data)))
        counts.setdefault(c1,0)
        #将该坐标点加入average中
        for i in range(len(row.data)):
            averages[c1][i]+=float(row.data[i])
            
        #记录每个分类中有多少个坐标点
        counts[c1] += 1
    #将总和除以计数值以求得平均值
    print averages
    print counts
    for c1,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[c1]
    return averages
        
def dotproduct(v1,v2):
    #求点积
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def dpclassify(point,avgs):
    #利用线性分类方法分类
    #求向量M0->M1和向量(M0+M1)/2->X的点积
    b = (dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
    y = dotproduct(point,avgs[0]) - dotproduct(point,avgs[1])+b
    if y>0:
        return 0
    else:
        return 1
    
def yesno(v):
    #是否问题，转化为数值型数据
    if v=='yes':
        return 1
    elif v=='no':
        return -1
    else:
        return 0
        
def matchcount(i1,i2):
    #将共同的兴趣爱好作为变量
    l1 = i1.split(':')      
    l2 = i2.split(':')
    x=0
    for v in l1:
        if v in l2:
            x+=1
    return x
        
def milesdistance(a1,a2):
    #返回约会者的距离数据
    return 0        
        
def loadnumerical():
    #利用上述辅助函数构造新数据集
    oldrows = loadmatch('matchmaker.csv')
    newrows = []
    for row in oldrows:
        d = row.data
        data = [float(d[0]),yesno(d[1]),yesno(d[2]),
                float(d[5]),yesno(d[6]),yesno(d[7]),
                     matchcount(d[3],d[8]),row.match]
        newrows.append(matchrow(data))
    return newrows
        
def scaledata(rows):
    low = [999999999.0]*len(rows[0].data)
    high = [-999999999.0]*len(rows[0].data) 
    
    #寻找最大值和最小值
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if d[i]<low[i]:
                low[i]=d[i]
            if d[i]>high[i]:
                high[i]=d[i]
    
    print low,high
    #对数据进行缩放处理的函数
    def scaleinput(d):
        return [(d[i]-low[i])/(high[i]-low[i]) for i in range(len(low))]
       
    #对所有数据进行缩放处理
    newrows = [matchrow(scaleinput(row.data)+[row.match]) for row in rows]
    
    #返回新的数据和缩放处理函数
    return newrows, scaleinput

'''核方法'''
def veclength(v):
  #向量各分量的平方和
  return sum([p**2 for p in v])

def rbf(v1,v2,gamma=20):
    dv = [v1[i]-v2[i] for i in range(len(v1))]
    l = veclength(dv)
    return math.e**(-gamma*l)   
  
def nlclassify(point,rows,offset,gamma=10):
    sum0=0.0
    sum1=0.0
    count0=0
    count1=0
    
    for row in rows:
        if row.match == 0:
            sum0+= rbf(point,row.data,gamma)
            count0+=1
        else:
            sum1+=rbf(point,row.data,gamma)
            count1+=1
    
    y = (1.0/count0)*sum0 - (1.0/count1)*sum1+offset
    if y<0:
        return 0
    else:
        return 1
    
def getoffset(rows,gamma=10):
    l0=[]
    l1=[]
    
    for row in rows:
        if row.match == 0:
            l0.append(row.data)
        else:
            l1.append(row.data)
    
    sum0 = sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
    sum1 = sum(sum([rbf(v1,v2,gamma) for v1 in l1]) for v2 in l1)
    
    return (1.0/(len(l1)**2))*sum1 - (1.0/(len(l0)**2))*sum0


        
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        