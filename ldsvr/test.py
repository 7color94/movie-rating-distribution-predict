#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
just for test
'''

import numpy as np
trainDistribution = np.loadtxt('trainDistribution.txt')

Ktest = np.loadtxt('Ktest.txt')
D = np.loadtxt('D.txt')
CVPredict = np.loadtxt('CVPredict.txt')
CVDistribution = np.loadtxt('CVDistribution.txt')

CVFeature = np.loadtxt('CVFeature.txt')
testFeature = np.loadtxt('testFeature.txt')
testPredict = np.loadtxt('testPredict.txt')

print testFeature.shape

i=0
'''
for row1 in testFeature:
    print row1[0], row1[1], row1[953], row1[954]
'''

for row1, row2 in zip(D, Ktest):
    print row1[0], ' ', row1[1], ' ', row1[2]
    print row2[0], ' ', row2[1], ' ', row2[2]
    print 
    i+=1
    if i==5:
        break

'''
t = np.array([[1,2,3,4,5,6],[7,8,9,10,11,12],[13,14,15,16,17,18],[19,20,21,22,23,24],[25,26,27,28,29,30]])
print t

l = np.array([0,2,4])
print l.shape
left = np.zeros(l.shape[0]**2, dtype=np.int)
right = np.zeros(l.shape[0]**2, dtype=np.int)
print left.shape
index = 0
for i in l:
    for j in l:
        left[index] = i
        right[index] = j
        index += 1
print l
print left
print right

print t[left, right]
'''