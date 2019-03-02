#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: LR.py
@author: dujiahao
@create_time: 2018/5/8 16:10
@description:调参 拟合线性回归模型 预测
"""
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.metrics import accuracy_score
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
    # x_dtrain, x_test, y_dtrain, y_test = train_test_split(dataset12_x, dataset12_y, random_state=1000, test_size=0.3)
    # lr = LogisticRegression(C=1.0,penalty='l2',solver='newton-cg',class_weight='balanced')
    # lr.fit(x_dtrain, y_dtrain)
    # predictions = lr.predict(x_test)
    # print('AUC',roc_auc_score(y_test, predictions))
    # print('准确率',accuracy_score(y_test,predictions))

    # 拟合模型
    # lr = LogisticRegression(C=1.0, penalty='l2', solver='newton-cg', class_weight='balanced')
    # lr.fit(dataset12_x, dataset12_y)
    # joblib.dump(lr, 'lr.model')  # 保存训练的RF模型
    # predict test set
    lr = joblib.load('lr.model')
    result = lr.predict_proba(dataset3_x)
    result = pd.DataFrame(result)
    result.index = dataset3.index
    result.columns = ['0', 'probability']
    result.drop('0',
                axis=1,
                inplace=True)
    dataset3_preds['label'] = result.copy()
    dataset3_preds.label = MinMaxScaler().fit_transform(dataset3_preds.label.reshape(-1, 1))
    dataset3_preds.sort_values(by=['Coupon_id', 'label'], inplace=True)
    dataset3_preds.to_csv("lr_preds.csv", index=None, header=None)
    print(dataset3_preds.describe())

    cost_time = time.time() - start_time
    print('cost_time', cost_time)




