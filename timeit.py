# -*- coding: utf-8 -*-
# @Time    : 18-7-25 上午11:16
# @Author  : Crazycosin
# @Site    : 
# @File    : timeit.py
# @Software: PyCharm
import timeit
def test():
    """Stupid test function"""
    L = [i for i in range(100)]

if __name__ == '__main__':
    print(timeit.timeit("test()", setup="from __main__ import test"))