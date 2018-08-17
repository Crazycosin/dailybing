# -*- coding: utf-8 -*-
# @Time    : 18-7-25 下午9:57
# @Author  : Crazycosin
# @Site    : 
# @File    : bignumber.py.py
# @Software: PyCharm
from threading import Thread,currentThread
'''
模拟310位求解，因为我不知道每10位求解。
我大致使用9位求解，每个线程求一位，第二个线程从倒数开始逐位变9
'''
def bignumber_calculator(bignumber,div):
    '''
    bignumber为被除数，
    div为除数，
    但循环计算余数，将余数用列表存储起来
    如果商为0计算完毕,如果不为0，除数加2
    :return:
    '''
    bignumber = float(bignumber)
    print('第%s线程循环计算%f'%(currentThread().getName(),bignumber))
    binary_list = []
    i = 0#循环计数器
    try:
        while bignumber//2>0:
            '''
            等于0时，说明还有一次计算过程
            '''
            binary_list.append(bignumber % 2)
            bignumber = bignumber//div
            div +=2
            i +=1
            print('第%s线程的第%d次循环计算结果div为%d'%(currentThread().getName(),i,div))
        print(" %s 线程结束" % currentThread().getName())
    except (RuntimeError, TypeError, NameError):
        print('第%s线程的第%d次循环计算出现错误'%(currentThread().getName(),i))
    file_name = currentThread().getName()+'计算结果.txt'
    fr = open(file_name,'w')
    for v in binary_list:
        s = str(v)+','
        fr.write(s)
    fr.close()
    return binary_list#返回存储余数的列表


if __name__ == "__main__":
    thread = []
    bignumber_str = '1'*9
    thread0 = Thread(name="calculator" + bignumber_str, \
                   target=bignumber_calculator, args=(bignumber_str,3))
    thread.append(thread0)
    for i in range(1,9):
        '''
        创建剩余8个线程
        '''
        #将i*10到（i+1）*10置9
        for j in (9-i,10-i):
            l = list(bignumber_str)
            l[j-1] = '9'
            bignumber_str = ''.join(l)  # 将列表重新连接为字符串
        t = Thread(name="calculator" + str(i), \
                   target=bignumber_calculator, args=(bignumber_str,3))

        thread.append(t)
    for k in thread:
        k.start()
    for i in thread:
        i.join()
        print("thread name:", i.name)
        print("alive:", i.is_alive())

