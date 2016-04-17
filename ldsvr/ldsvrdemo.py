#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ldsvr import ldsvrmsvr, kernelmatrix
import numpy as np
from scipy import spatial

def ldsvrtrain(trainFeature, trainDistribution, para):
    '''
    inputs:
        trainFeature: training examples (m x d)
        trainDistribution: training labels (m x k)
        para: parameters needed for the training period
    outputs:
        modelpara: parameters of the LDSVR model
    '''
    (Beta, b, svindex) = ldsvrmsvr(trainFeature, trainDistribution, para)
    modelpara = {}
    modelpara['svindex'] = svindex
    modelpara['Beta'] = Beta
    modelpara['b'] = b
    modelpara['ker'] = para['ker']
    modelpara['par'] = para['par']
    return modelpara


def ldsvrpredict(testFeature, trainFeature, modelpara):
    '''
    inputs:
        testFeature: data matrix with test samples in rows and features in in columns (c x d)
        trainFeature: data matrix with training samples in rows and features in columns (m x d)
        modelpara: model parameters of LDSVR model.
    outputs:
        predict: prediction of testFeature's label distribution.
    '''
    # compute kernel matrix for prediction using testFeature and trainFeature
    Ktest = kernelmatrix(modelpara['ker'], modelpara['par'], trainFeature.T, testFeature.T)
    np.savetxt('Ktest.txt', Ktest)
    print 'save Ktest'
    # prediction
    predict = Ktest.dot(modelpara['Beta']) + np.tile(modelpara['b'], (Ktest.shape[0],1))
    # use sigmoid function to the predicted label distribution
    predict = 1.0 / (1.0 + np.exp(-predict))
    # normalization for the predicted label distribution
    predict = predict / np.tile(np.sum(predict, axis=1, keepdims=1), (1, predict.shape[1]))
    return predict


def run():
    # load the trainFeature, trainDistribution, testFeature
    features = np.loadtxt('features.txt')
    distributions = np.loadtxt('distributions.txt')
    trainFeature = features[259:]
    trainDistribution = distributions[259:]
    # CVFeature = features[0:259]
    # CVDistribution = distributions[0:259]
    testFeature = np.loadtxt('testFeature.txt')
    print 'read trainFeature, trainDistribution, CVFeature done.'

    # initialize the model parameters.
    para = {}
    # tolerance during the iteration
    para['tol']=np.e**-10
    # instances whose distance computed is more than epsi should be penalized
    para['epsi']=0.1
    # penalty parameter
    para['C']=1
    # type of kernel function ('lin', 'poly', 'rbf', 'sam')
    para['ker']='rbf'
    # parameter of kernel function
    para['par']=1*np.mean(spatial.distance.pdist(trainFeature))
    print para['par']

    Beta = np.loadtxt('Beta.txt')
    b = np.loadtxt('b.txt')
    modelpara = {}
    if Beta.size != 0 and b.size != 0 :
        print 'read Beta&&b from files'
        modelpara['Beta'] = Beta
        modelpara['b'] = b
        modelpara['ker'] = para['ker']
        modelpara['par'] = para['par']
    else:
        print 'begin train.'
        modelpara = ldsvrtrain(trainFeature, trainDistribution, para)
        print 'train done.'
        np.savetxt('Beta.txt', modelpara['Beta'])
        np.savetxt('b.txt', modelpara['b'])
        print 'write Beat&b to files.'

    # prediction
    # use trained model parameters to predict the distribution.
    testPredict = ldsvrpredict(testFeature, trainFeature, modelpara);
    np.savetxt('trainFeature.txt', trainFeature)
    np.savetxt('trainDistribution.txt', trainDistribution)
    # np.savetxt('CVFeature.txt', CVFeature)
    # np.savetxt('CVDistribution.txt', CVDistribution)
    # np.savetxt('CVPredict.txt', CVPredict)
    np.savetxt('testPredict.txt', testPredict)
    print 'test predict done.'


if __name__ == '__main__':
    run()
