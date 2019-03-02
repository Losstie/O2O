#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: weightBlender.py
@author: dujiahao
@create_time: 2018/5/23 23:01
@description:
"""
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
import pandas as pd
import numpy as np
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
import xgboost as xgb
from sklearn.externals import joblib
from pylab import mpl
import time

start_time = time.time()

if __name__ == '__main__':
    clf_svm = joblib.load('svm.model')
    clf_rf = joblib.load('rf.model')
    clf_lr = joblib.load('lr.model')


    dataset3 = pd.read_csv(r'F:\Project\FinaDesigner_Dujiahao\data\dataset3.csv')
    dataset3.replace(np.nan, 0, inplace=True)
    dataset3.replace(np.inf, 0, inplace=True)
    dataset3.drop_duplicates(inplace=True)

    dataset3_preds = dataset3[['User_id', 'Coupon_id', 'Date_received']]
    dataset3_x = dataset3.drop(['User_id', 'Coupon_id', 'Date_received'], axis=1)

    result_svm = clf_svm.predict(dataset3_x)
    result_rf = clf_rf.predict(dataset3_x)
    result_lr = clf_lr.predict(dataset3_x)

    dataset3 = pd.read_csv(r'F:\Project\FinaDesigner_Dujiahao\data\dataset3.csv')
    dataset3.drop_duplicates(inplace=True)
    dataset3_x = dataset3.drop(['User_id', 'Coupon_id', 'Date_received'], axis=1)
    dataset3 = xgb.DMatrix(dataset3_x)
    clf_xgb = xgb.Booster(model_file='xgb.model')

    result_xgb = clf_xgb.predict(dataset3)
    w1 = 0.05
    w2 = 0
    w3 = 0.05
    w4 = 0.9
    result = w1*result_svm + w2*result_rf + w3*result_lr + w4*result_xgb
    print(w1, w2, w3, w4)
    print(result)
    dataset3_preds['label'] = result
    dataset3_preds.label = MinMaxScaler().fit_transform(dataset3_preds.label.reshape(-1, 1))
    dataset3_preds.sort_values(by=['Coupon_id', 'label'], inplace=True)
    dataset3_preds.to_csv("weightfusion_preds.csv", index=None, header=None)
    print(dataset3_preds.describe())

    cost_time = time.time() - start_time
    print('cost_time', cost_time)
