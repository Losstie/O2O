#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: ser.py
@author: dujiahao
@create_time: 2018/5/9 11:34
@description: 便于web展示训练过程
"""
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
import time
import json
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
# 程序开始时间
start_time = time.time()

params = {
    'booster': 'gbtree',
    'objective': 'rank:pairwise',
    'eval_metric': 'auc',
    'gamma': 0.1,
    'min_child_weight': 1.1,
    'max_depth': 5,
    'lambda': 10,
    'subsample': 0.8,
    'colsample_bytree': 0.7,
    'colsample_bylevel': 0.7,
    'eta': 0.01,
    'tree_method': 'exact',
    'seed': 0,
    'nthread': 12
}

file_name = r'F:\Project\FinaDesigner_Dujiahao\auc_change.json'
data = {
    'history_auc':[],
    'history_rouns':[]
}

def callback_draw(env):
    # "用于每次迭代结束时候刷新auc变化曲线"
    result_list = env.evaluation_result_list
    n_rounds = env.iteration + 1
    score = result_list[0][1]

    if(n_rounds % 5 ==0):
        data['history_auc'].append(score)
        data['history_rouns'].append(n_rounds)
        with open(file_name, 'w') as file_obj:
            '''写入json文件'''
            json.dump(data, file_obj)


if __name__ == '__main__':
    "主函数"

    dataset1 = pd.read_csv(r'F:\Project\FinaDesigner_Dujiahao\data\dataset1.csv')
    dataset1.label.replace(-1, 0, inplace=True)
    dataset2 = pd.read_csv(r'F:\Project\FinaDesigner_Dujiahao\data\dataset2.csv')
    dataset2.label.replace(-1, 0, inplace=True)
    dataset3 = pd.read_csv(r'F:\Project\FinaDesigner_Dujiahao\data\dataset3.csv')

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

    dataset1 = xgb.DMatrix(dataset1_x, label=dataset1_y)
    dataset2 = xgb.DMatrix(dataset2_x, label=dataset2_y)
    dataset12 = xgb.DMatrix(dataset12_x, label=dataset12_y)
    dataset3 = xgb.DMatrix(dataset3_x)
    watchlist = [(dataset12, 'train')]
    model = xgb.train(params, dataset12, num_boost_round=4600, evals=watchlist,early_stopping_rounds=50,callbacks=[callback_draw])
    dataset3_preds['label'] = model.predict(dataset3)
    dataset3_preds.label = MinMaxScaler().fit_transform(dataset3_preds.label.reshape(-1, 1))
    dataset3_preds.sort_values(by=['Coupon_id', 'label'], inplace=True)
    dataset3_preds.to_csv("xgb_preds.csv", index=None, header=None)
    print(dataset3_preds.describe())

    cost_time = time.time() - start_time
    print("cost_time:", cost_time)