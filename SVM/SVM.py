#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: SVM.py
@author: dujiahao
@create_time: 2018/5/8 16:10
@description:
"""
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn import svm
from sklearn.metrics import roc_auc_score
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import time
from sklearn.model_selection import train_test_split
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体

# 程序开始时间
start_time = time.time()

if __name__ == '__main__':
    "主函数"

    dataset1 = pd.read_csv('data/dataset1.csv')
    dataset1.label.replace(-1, 0, inplace=True)
    dataset1.replace(np.nan,0,inplace=True)
    dataset1.replace(np.inf,0,inplace=True)
    dataset2 = pd.read_csv('data/dataset2.csv')
    dataset2.label.replace(-1, 0, inplace=True)
    dataset2.replace(np.inf,0,inplace=True)
    dataset2.replace(np.nan,0,inplace=True)
    dataset3 = pd.read_csv('data/dataset3.csv')
    dataset3.replace(np.nan, 0,inplace=True)
    dataset3.replace(np.inf, 0,inplace=True)

    dataset1.drop_duplicates(inplace=True)
    dataset2.drop_duplicates(inplace=True)
    dataset3.drop_duplicates(inplace=True)
    dataset12 = pd.concat([dataset1, dataset2], axis=0)

    dataset1_y = dataset1.label
    dataset1_x = dataset1.drop(['User_id', 'label',],axis=1)
    dataset2_y = dataset2.label
    dataset2_x = dataset2.drop(['User_id', 'label'], axis=1)
    dataset12_y = dataset12.label
    dataset12_x = dataset12.drop(['User_id', 'label'], axis=1)
    dataset3_preds = dataset3[['User_id', 'Coupon_id', 'Date_received']]
    dataset3_x = dataset3.drop(['User_id', 'Coupon_id','Date_received'], axis=1)
    print(dataset1_x.shape, dataset2_x.shape, dataset3_x.shape)

    # 调参
    # 归一化
    Normalizer().fit_transform(dataset12_x)
    # 划分训练集和测试集
    # x_dtrain, x_deval, y_dtrain, y_deval = train_test_split(dataset12_x, dataset12_y, random_state=1000,test_size=0.3)
    clf = svm.LinearSVR(C=1, epsilon=0.5,random_state=0)
    # clf = clf.fit(x_dtrain, y_dtrain)
    # y_pred = clf.predict(x_deval)
    # print(y_pred)
    # print('测试集auc得分',roc_auc_score(y_deval,y_pred))

    # 拟合模型
    clf = clf.fit(dataset12_x,dataset12_y)
    joblib.dump(clf, 'svm.model')  # 保存训练的svm模型

    # predict test set
    # clf = joblib.load('svm.model')
    dataset3_preds['label'] = clf.predict(dataset3_x)
    dataset3_preds.label = MinMaxScaler().fit_transform(dataset3_preds.label.reshape(-1, 1))
    dataset3_preds.sort_values(by=['Coupon_id', 'label'], inplace=True)
    dataset3_preds.to_csv("svm_preds.csv", index=None, header=None)
    print(dataset3_preds.describe())

    cost_time = time.time() - start_time
    print('cost_time', cost_time)