import  pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

filename = 'F:\pythonprojects\Assignment3\data.csv'
data = pd.read_csv(filename)
#继续使用上次的数据集，观察“成交量激增时刻”因子对于数字货币交易的rank能力

def rank(A,N,m):
    #数字货币A(eg:1)的指标m（eg：H代表最高价）在时间节点N在所有货币中的排序值
    range=[]
    for i in range(0,8):
        range.append(data.iloc[N-i][str(m)+str(A)])
    return rank(range)[A-1]

def adv(A,N,n):
    #数字货币A在时间节点N往前n天的平均成交量
    sum=0
    if(N<=n):
        n=N
    for i in range(0,n):
        sum=sum+data.iloc[N-i]["V"+str(A)]
    return sum/n

def Judge(X,Y,Z):
    #若X成立则返回Y，否则返回Z
    if X is True:
        return Y
    else:
        return Z

def returns(A,N):
    #数字货币A在时间节点N的相对昨日收益率
    return data.iloc[N]["C"+str(A)]/data.iloc[N-1]["C"+str(A)]-1

def VWAP(A,N,n):
    #数字货币A在时间节点N往前n天的加权成交价
    sum = 0
    value=0
    if (N <= n):
        n = N
    for i in range(0, n):
        sum = sum + data.iloc[N - i]["V" + str(A)]
        value = value+data.iloc[N - i]["V" + str(A)]*data.iloc[N - i]["C" + str(A)]
    return value / sum

def delay(A,N,m,d):
    #数字货币A的指标m在时间节点N往前d天的值
    if (N< d):
        d=N
    return data.iloc[N-d][str(m)+str(A)]

def delta(A,N,m,d):
    #数字货币A的指标m在时间节点N的值相对往前d天的值的增量
    return data.iloc[N][str(m)+str(A)]-delay(A,N,m,d)

def delta_mean(A,N,m,n):
    #数字货币A的指标m在时间节点N的值相对往前一天的值的增量的n天平均值
    sum = 0
    if (N <= n):
        n = N
    for i in range(0, n):
        sum=sum+delta(A,N,m,1)
    return sum/n

def delta_std(A,N,m,n):
    ##数字货币A的指标m在时间节点N的值相对往前一天的值的增量的n天标准差
    sum = 0
    if (N <= n):
        n = N
    for i in range(0, n):
        sum = sum + (delta(A, N, m, 1)-delta_mean(A,N,m,n))**2
    return (sum / n)**0.5

#为了方便分别定义数字货币A在时间节点N的各个指标
def O(A,N):
    return data.iloc[N]["O"+str(A)]

def H(A,N):
    return data.iloc[N]["H"+str(A)]

def L(A,N):
    return data.iloc[N]["L"+str(A)]

def C(A,N):
    return data.iloc[N]["C"+str(A)]

def V(A,N):
    return data.iloc[N]["V"+str(A)]

def fastIncrese(A,N):#定义时间节点N处数字货币A的激增因子值
    if(delta(A,N,'O',1)>delta_mean(A,N,'C',5)+delta_std(A,N,'C',5)):
        return 1
    else:
        return 0

def fastIncrese24(A,N):#定义时间节点N处往前5个节点数字货币A激增因子值计数
    sum = 0
    n=5
    if (N <= 5):
        n = N
    for i in range(0, n):
        sum=sum+fastIncrese(A,N-i)
    return sum

def factor101(A,N):#定义时间节点N处数字货币A的101号因子值
    return V(A,N)*(C(A,N)-O(A,N))/((H(A,N)-L(A,N))+0.01)

def newfactor(A,N):#等权赋予新因子，由于激增因子为正整数
    return fastIncrese24(A,N)*factor101(A,N)

stat=pd.DataFrame(columns=['1','2','3','4','5','6','7','8'])

for i in range(0,2048):
    stat.loc[i]={'1':fastIncrese24(1,i)*factor101(1,i),'2':fastIncrese24(2,i)*factor101(2,i),
                 '3':fastIncrese24(3,i)*factor101(3,i),'4':fastIncrese24(4,i)*factor101(4,i),
                 '5':fastIncrese24(5,i)*factor101(5,i),'6':fastIncrese24(6,i)*factor101(5,i),
                 '7':fastIncrese24(7,i)*factor101(7,i),'8':fastIncrese24(8,i)*factor101(8,i)}
    print(stat.loc[i])
stat.to_csv('newfactor.csv')

buy=[]#用于接受每个节点购买的货币编号
for i in range(0,2048):
    min=1
    for j in range(1,9):
        if(stat.values[i][j-1]<=stat.values[i][min-1]):
            min=j
    buy.append(min)
    print(min)

values=[]
values.append(10000)
for i in range(1,2048):
    values.append(values[i-1]*data.iloc[i]["C"+str(buy[i-1])]/data.iloc[i-1]["C"+str(buy[i-1])])
    print(i)
x=range(0,2048)
plt.plot(x,values)
plt.show()#画出净值曲线
