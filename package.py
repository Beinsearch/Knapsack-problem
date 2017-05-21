#-*-coding:utf-8-*-
import numpy as np
from time import clock

#递归
def package_recursion(volume,value,capacity):
    l = len(volume)
    if capacity==0:return np.zeros(l,dtype=int)
    if l == 1:
        if volume[0]<=capacity:return [1]
        else:return [0]
    if volume[0]>capacity:
        return np.append(0,package_recursion(volume[1:],value[1:],capacity))
    s1 = package_recursion(volume[1:],value[1:],capacity-volume[0])
    s2 = package_recursion(volume[1:],value[1:],capacity)
    v1 = (s1*value[1:]).sum()
    v2 = (s2*value[1:]).sum()
    if value[0]+v1>v2:
        return np.append(1,s1)
    else:
        return np.append(0,s2)

#动态规划
def package_dynamicplanning(weight,value,capacity):
    l = len(weight)
    minw = min(weight)
    sumw = sum(weight)
    blank = [0]*l
    if capacity < minw:
        return blank
    if capacity >= sumw:
        return [1]*l

    sol = {}
    #解字典，sol[背包重量限制_前i个物品]=[最大价值,选择的物品列表]
    #初始化
    for j in range(0,capacity+1):
        for i in range(l):              
            sol.setdefault('_'.join([str(j),str(i)]),[0,blank])
    #只能选第一个物品时，当背包足够大，所能收纳的最大价值为value[0]
    blank2 = blank[:]
    blank2[0] = 1      
    for j in range(1,capacity+1):
        if j>=weight[0]:    
            sol['_'.join([str(j),'0'])] = [value[0],blank2]
            
    for j in range(1,capacity+1):
        for i in range(1,l):
            if weight[i] > j:   #第i个物品超出背包容量限制
                sol['_'.join([str(j),str(i)])] = sol['_'.join([str(j),str(i-1)])]
            else:
                v1 = sol['_'.join([str(j),str(i-1)])][0]
                v2 = sol['_'.join([str(j-weight[i]),str(i-1)])][0]+value[i]
                if v1 >= v2:
                    sol['_'.join([str(j),str(i)])] = sol['_'.join([str(j),str(i-1)])]
                else:
                    index = sol['_'.join([str(j-weight[i]),str(i-1)])][1][:]
                    index[i] = 1
                    sol['_'.join([str(j),str(i)])] = [v2,index]
                    
   return sol['_'.join([str(capacity),str(l-1)])][1]

##vol = np.array([17, 4, 12,  9])
##val = np.array([12, 7, 14, 15])
##cap = 25

size= 20
vol = np.random.randint(1,100,size)
val = np.random.randint(1,100,size)
cap = int(vol.sum()*0.6)
print 'volume vector:%s' % vol
print 'value  vector:%s' % val
print 'capacity     :%d' % cap

t = clock()
s = package_dynamicplanning(vol,val,cap)
print 'dynamicplanning time:%.2fs' % (clock()-t)
print 'scheme       :%s' % np.array(s)
print 'total volume :%d' % (s*vol).sum()
print 'total value  :%d' % (s*val).sum()

t = clock()
s = package_recursion(vol,val,cap)
print 'recursion time:%.2fs' % (clock()-t)
print 'scheme       :%s' % s
print 'total volume :%d' % (s*vol).sum()
print 'total value  :%d' % (s*val).sum()
