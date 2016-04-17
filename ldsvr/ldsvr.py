#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def kernelmatrix(ker, parameter, trainFeature, testFeature):
    '''
    function:
        kernelmatrix
        calculate the kernel matrix of the instance vectors in testFeature and trainFeature
    inputs:
        ker: type of kernel function ('lin', 'poly', 'rbf', 'sam')
        parameter: parameters of kernel function
        trainFeature: data matrix with training samples in columns and features in rows (d x m)
        testFeature: data matrix with test samples in columns and features in in rows (d x c)
    outputs:
        k: kernel matrix, each element corresponds to the kernel of two feature vectors (c x m)
    Extended description of input/ouput variables
        PARAMETER:
            SIGMA: width of the RBF and sam kernel
            BIAS: bias in the linear and polinomial kernel
            DEGREE: degree in the polynomial kernel
    '''
    k = None
    if ker == 'lin':
        print 'lin kernel.'
        if trainFeature.size != 0:
            k = testFeature.T.dot(trainFeature) + parameter
        else:
            k = testFeature.T.dot(testFeature) + parameter
    elif ker == 'poly':
        print 'poly kernel.'
        if trainFeature.size != 0:
            k = (testFeature.T.dot(trainFeature) + 1) ** parameter
        else:
            k = (testFeature.T.dot(testFeature) + 1) ** parameter
    elif ker == 'rbf':
        # To speed up the computation of the RBF kernel matrix, 
        # we exploit a decomposition of the Euclidean distance (norm).
        # compute x^2
        print 'rbf kernel.'
        D = None
        n1sq = np.sum(testFeature**2, axis=0, keepdims=1) # 1 x ..
        n1 = testFeature.shape[1]
        if trainFeature.size == 0:
            # ||x-y||^2 = x^2 + y^2 - 2*x'*y 
            D = (np.ones((n1,1), dtype=np.double).dot(n1sq)).T + np.ones((n1,1), dtype=np.double).dot(n1sq) - 2*testFeature.T.dot(testFeature);
        else:
            print 'trainFeature size != 0'
            n2sq = np.sum(trainFeature**2, axis=0, keepdims=1)
            n2 = trainFeature.shape[1]
            # ||x-y||^2 = x^2 + y^2 - 2*x'*y 
            D = (np.ones((n2, 1), dtype=np.double).dot(n1sq)).T + np.ones((n1,1), dtype=np.double).dot(n2sq) - 2*testFeature.T.dot(trainFeature)
        np.savetxt('D.txt', D)
        print 'debug: save D'
        k = np.exp(-D/(2.0*parameter*parameter))
    elif ker == 'sam':
        print 'sam kernel.'
        if trainFeature.size != 0:
            D = testFeature.T.dot(trainFeature)
        else:
            D = testFeature.T.dot(testFeature)
        k = np.exp((-np.arccos(D)**2).dot(np.linalg.inv(2*parameter.dot(parameter))))
    else:
        print 'Unsupported kernel: ', ker
    return k


def ldsvrmsvr(x, y, para):
    '''
    function:
        ldsvr
    inputs:
        x: m x d
        y: m x k
        para: model parameters of LDSVR model.
    outputs:
        beta: coeficient matrix of trainFeature's linear combination (m x k)
        b: intercept matrix (1 x k)
        svindex: support vectors' subscripts of row in trainFeature (n x 1)
    extended description of inputs/ouputs variables
    para:
        para.tol: tolerance during the iteration
        para.epsi: instances whose distance computed is more than epsi should be penalized
        para.C: penalty parameter
        para.ker: type of kernel function ('lin', 'poly', 'rbf', 'sam')
        para.par: parameters of kernel function
            SIGMA: width of the RBF and sam kernel
            BIAS: bias in the linear and polinomial kernel
            DEGREE: degree in the polynomial kernel
    '''
    # process the trainDistribution
    n_k = y.shape[1]
    zero = np.where(y==0)
    # avoid the error of dividing zero
    y[zero] = y[zero] + 1.0/(n_k*10)
    # normalization
    y = y / np.tile(np.sum(y.T, axis=0, keepdims=1).T, (1, n_k))
    # use sigmodi function to the trainDistribution
    y = -np.log(1.0/y - 1)
    print 'process the trainDistribution done.'

    n_m = x.shape[0]
    n_k = y.shape[1]

    '''
    default value of para
    para['tol']=10^-20;
    para['epsi'] = 1;
    para['C'] = 1;
    para['par'] = 0.01;
    para['ker'] = 'rbf';
    '''
    # build the kernel matrix on the labeled samples (m x m)
    H = kernelmatrix(para['ker'], para['par'], x.T, x.T)

    # create matrix for regression parameters
    # w(j) may be represented as a linear combination of the training examples in the feature space
    Beta = np.zeros((n_m, n_k))
    # b(k) corresponds to y(:k)
    b = np.zeros((1, n_k))

    # E = prediction error per output (m x k)
    E = y - H.dot(Beta) - np.tile(b, (n_m,1))
    # compute Euclidean distance of each examples
    # u = RSE (m x 1)
    u = np.sqrt(np.sum(E**2, axis=1, keepdims=1)) # ???
    # use u_z to substitute u_d
    # u_z: m x 1
    u_z = u/4.0;

    # RMSE
    RMSE = np.zeros((1000000,1), dtype=np.double)
    RMSE[1,0] = np.sqrt(np.mean(u_z**2, axis=0)) # u_z:m x 1, 不需要keepdims

    # points for which prediction error is larger than epsilon
    # i.e., find SVs whose loss function != 0
    i1 = np.where(u_z >= para['epsi'])
    # print 'i1: \n', i1

    # set initial values of alphas (m x 1)
    a = para['C']*(u_z-4*para['epsi']) / (4*u_z)

    # compute loss function matrix by definition
    # L is the loss function matrix (m x 1)
    L = np.zeros(u_z.shape, dtype=np.double)
    # we modify only entries for which  u_z > epsi.
    L[i1] = u_z[i1]**2 - 2*para['epsi']*u_z[i1] + para['epsi']**2

    # Lp is the quantity to minimize (sq norm of parameters + slacks)
    Lp = np.zeros((1000000,1), dtype=np.double)
    # Beta: m x k
    # np.diag --> k x 1, 不需要keepdims
    Lp[1, 0] = np.sum(np.diag(Beta.T.dot(H).dot(Beta)), axis=0)/2 + para['C']*np.sum(L, axis=0)

    # initial variables used in loop
    # step length
    eta = 1
    # iteration number
    k = 1
    # sentinel of loop
    hacer = 1
    # sign of whether find support vectors
    val = 1

    print 'begin train looping.'

    # start training
    while hacer == 1:
        # print the iteration information.
        print 'iter: %4d, Lp: %15.7f, RMSE: %15.7f' % (k, Lp[k, 0], RMSE[k, 0])
        # next iteratio
        k = k+1
        # save the model parameters in the previous step
        Beta_a = Beta
        b_a = b
        i1_a = i1

        # [H+inv(D_a), 1; a'*H, 1'*a]*[Beta(:j); b(j)] = [y(:j); a'*y(:j)] 
        # M1 = [H+inv(D_a), 1; a'*H, 1'*a] (only for obs i1. see above)
        # 假设i1: _m x 1 
        # a: m x 1 ; a[i1]: (_m,) matlab中_m x 1, 使用_a代替a[i1]; np.diag(a(i1)) --> _m x _m
        # u_z: m x 1 ; ; _m <= m ; H: m x m
        # H(i1, i1): _m x _m
        _a = a[i1].reshape(-1, 1) # 这是由于python和matlab不同所导致
        _m = a[i1].shape[0]
        '''
        # print 'a[i1]: ', a[i1].shape
        _one_D_a = a[i1].reshape(_m)
        # print '_one_D_a: ', _one_D_a.shape
        '''
        D_a_inv = np.diag(1/a[i1])
        # print 'D_a_inv: ', D_a_inv.shape

        # row_i1: (_m, )
        row_i1 = i1[0]
        left_i1 = np.zeros(row_i1.shape[0]**2, dtype=np.int)
        right_i1 = np.zeros(row_i1.shape[0]**2, dtype=np.int)
        index = 0
        for _left_i1 in row_i1:
            for _right_i1 in row_i1:
                left_i1[index] = _left_i1
                right_i1[index] = _right_i1
                index += 1
        _K = H[left_i1, right_i1].reshape(_m, _m)
        # print '_K: ', _K.shape
        # 求解M1的左上角元素
        # M1: _m x _m
        M1 = _K + D_a_inv
        # 列组合：M1(_m x _m) 和 ones(_m x 1) --> _m x (_m + 1)
        M1 = np.column_stack((M1, np.ones((M1.shape[0],1), dtype=np.double)))
        # a: m x 1 ; a[i1]即_a: _m x 1
        # temp: 列组合，1 x _m x _m x _m --> 1 x _m 和 1 x 1
        # temp: 1 x (_m + 1)
        temp = np.column_stack((_a.T.dot(_K), np.sum(_a, axis=0, keepdims=1)))
        # 行组合: _m x (_m + 1) 和 1 x (_m + 1)
        # M1: (_m + 1) x (_m + 1)
        M1 = np.row_stack((M1, temp))
        M1 = M1 + np.e**(-11)*np.identity(M1.shape[0])

        # compute Beta and b (only for obs i1. see above)   
        # row_i1: (_m, )
        # y[row_i1,:]: (_m, k) ; a(i1).T.dot(y[i1,:])): 1 x _m x _m x k --> 1 x k
        # sal1: (_m + 1) x (_m + 1) x (_m + 1) x k --> (_m + 1) x k
        sal1 = np.linalg.inv(M1).dot(np.row_stack((y[row_i1,:], _a.T.dot(y[row_i1,:]))))
        b_sal1 = sal1[-1,:]
        b = b_sal1
        # sal1: _m x k
        sal1 = sal1[0:-1,:]
        # Beta: m x k
        Beta = np.zeros(Beta.shape, dtype=np.double)
        Beta[row_i1,:] = sal1

        # recompute error
        E = y-H.dot(Beta) - np.tile(b, (n_m,1))
        # recompute i1 and u_z
        u = np.sqrt(np.sum(E**2, axis=1, keepdims=1))
        u_z = u/4.0;
        i1 = np.where(u_z >= para['epsi'])
        # recompute loss function
        L = np.zeros(u_z.shape, dtype=np.double)
        L[i1] = u_z[i1]**2 - 2*para['epsi']*u_z[i1] + para['epsi']**2
        Lp[k, 0] = np.sum(np.diag(Beta.T.dot(H).dot(Beta)), axis=0)/2 + para['C']*np.sum(L, axis=0)

        # initial step length
        eta = 1
        while Lp[k, 0] > Lp[k-1, 0]:
            print 'enter eta loop.'
            # modify step length
            eta = eta/10;
            # restore i1
            i1 = i1_a
            # Beta: m x k
            Beta = np.zeros(Beta.shape)
            # the new betas are a combination of the current (sal1) and of the
            # previous iteration (Beta_a)
            # sal1: _m x k
            Beta[row_i1,:] = eta*sal1 + (1-eta)*Beta_a[row_i1,:]
            b = eta*b_sal1 + (1-eta)*b_a

            # recoumpte
            E = y - H.dot(Beta) - np.tile(b, (n_m,1))
            u_z = np.sqrt(np.sum(E**2, axis=1, keepdims=1))
            u_z = u_z/4
            i1 = np.where(u_z >= para['epsi'])

            L = np.zeros(u_z.shape, dtype=np.double)
            L[i1] = u_z[i1]**2 - 2*para['epsi']*u_z[i1] + para['epsi']**2
            # recomputer Lp in kth iteration 
            Lp[k, 0] = np.sum(np.diag(Beta.T.dot(H).dot(Beta)), axis=0)/2 + para['C']*np.sum(L, axis=0)
            
            # stopping criterion #1
            if eta < 10**-16:
                print 'stop criterion 1: meet eta(step length) condition -> eta<10^-16.'
                print 'finally, Lp: %15.7f' % (Lp[k, 0])
                Lp[k, 0] = Lp[k-1, 0] - 10**-15
                Beta = Beta_a
                b = b_a
                i1 = i1_a
                # stop loop
                hacer = 0

        # here we modify the alphas
        a_a = a
        a = para['C']*(u_z-4*para['epsi']) / (4*u_z)
        RMSE[k, 0] = np.sqrt(np.mean(u_z**2, axis=0))

        # stopping criterion #2
        if (Lp[k-1, 0]-Lp[k, 0])/Lp[k-1, 0] < para['tol']:
            print 'stop criterion 2: meet tolerance condition -> Lp(k-1,1)-Lp(k,1))/Lp(k-1,1)<tol\n'
            hacer = 0

        # stopping criterion #3 - algorithm does not converge. (val = -1)
        if i1[0].size == 0:
            print 'stop criterion 3: algorithm does not converge (find no SVs).\n'
            Beta = np.zeros(Beta.shape)
            b = np.zeros(b.shape)
            i1 = []
            val = -1
            hacer = 0

    svindex = i1
    return (Beta, b, svindex)