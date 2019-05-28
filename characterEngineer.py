#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: characterEngineer.py
@author: dujiahao
@create_time: 2018/4/16 16:51
@description: 特征工程
"""


import pandas as pd
import numpy as np
import datetime as date



##################################拟合数据集#########################################
def get_label(s):
    s = s.split(':')
    if s[0] == 'null':
        return 0
    elif (date.date(int(s[0][0:4]),int(s[0][4:6]),int(s[0][6:8]))-date.date(int(s[1][0:4]),int(s[1][4:6]),int(s[1][6:8]))).days <= 15:
        return 1
    else:
        return -1


other_feature3 = pd.read_csv('characterEngineer/other_feature3.csv')
coupon3 = pd.read_csv('characterEngineer/coupon3_feature.csv')
merchant3 = pd.read_csv('characterEngineer/merchant3_feature.csv')# Merchant_id
user3 = pd.read_csv('characterEngineer/user3_feature.csv')# User_id
user_merchant3 = pd.read_csv('characterEngineer/user_merchant3_feature.csv')# User_id,Merchant_id
dataset3 = pd.merge(coupon3,other_feature3,on=['User_id','Merchant_id','Coupon_id','Date_received'],how='left')
dataset3 = pd.merge(dataset3,merchant3,on='Merchant_id',how='left')
dataset3 = pd.merge(dataset3,user3,on='User_id',how='left')
dataset3 = pd.merge(dataset3,user_merchant3,on=['User_id','Merchant_id'],how='left')
dataset3.drop_duplicates(inplace=True)
print(dataset3.shape,dataset3.columns.values.tolist())


dataset3.user_merchant_sales_count = dataset3.user_merchant_sales_count.replace(np.nan,0)
dataset3.user_same_merchant_coupon_counts = dataset3.user_same_merchant_coupon_counts .replace(np.nan, 0)
dataset3.diff_merchant_count = dataset3.diff_merchant_count.replace(np.nan, 0)
dataset3['is_weekend'] = dataset3.day_of_week.apply(lambda x:1 if x in (6,7) else 0)
weekday_dummies = pd.get_dummies(dataset3.day_of_week)
weekday_dummies.columns = ['weekday'+str(i+1) for i in range(weekday_dummies.shape[1])]
dataset3 = pd.concat([dataset3,weekday_dummies],axis=1)
dataset3.drop(['Merchant_id','day_of_week','coupon_count'],axis=1,inplace=True)
dataset3 = dataset3.replace('null',np.nan)
dataset3.to_csv('data/dataset3.csv',index=False)



coupon2 = pd.read_csv('characterEngineer/coupon2_feature.csv')
merchant2 = pd.read_csv('characterEngineer/merchant2_feature.csv')
user2 = pd.read_csv('characterEngineer/user2_feature.csv')
user_merchant2 = pd.read_csv('characterEngineer/user_merchant2_feature.csv')
other_feature2 = pd.read_csv('characterEngineer/other_feature2.csv')

dataset2 = pd.merge(coupon2,other_feature2,on=['User_id','Merchant_id','Coupon_id','Date_received'],how='left')
dataset2 = pd.merge(dataset2,merchant2,on='Merchant_id',how='left')
dataset2 = pd.merge(dataset2,user2,on='User_id',how='left')
dataset2 = pd.merge(dataset2,user_merchant2,on=['User_id','Merchant_id'],how='left')
dataset2.drop_duplicates(inplace=True)
print(dataset2.shape, dataset2.columns.values.tolist())

dataset2.user_merchant_sales_count  = dataset2.user_merchant_sales_count.replace(np.nan,0)
dataset2.user_same_merchant_coupon_counts = dataset2.user_same_merchant_coupon_counts.replace(np.nan,0)
dataset2.diff_merchant_count = dataset2.diff_merchant_count.replace(np.nan,0)
dataset2['is_weekend'] = dataset2.day_of_week.apply(lambda x:1 if x in (6,7) else 0)
weekday_dummies = pd.get_dummies(dataset2.day_of_week)
weekday_dummies.columns = ['weekday'+str(i+1) for i in range(weekday_dummies.shape[1])]
dataset2 = pd.concat([dataset2,weekday_dummies],axis=1)
dataset2 = dataset2.replace(np.nan,"null")
dataset2['label'] = dataset2.Date.astype('str') + ':' +  dataset2.Date_received.astype('str')
# print(dataset2.User_id)
print(dataset2.label)
dataset2.label = dataset2.label.apply(get_label)
dataset2.drop(['Merchant_id','day_of_week','Date','Date_received','Coupon_id','coupon_count'],axis=1,inplace=True)
dataset2 = dataset2.replace('null',np.nan)
dataset2.to_csv('data/dataset2.csv',index=None)

coupon1 = pd.read_csv('characterEngineer/coupon1_feature.csv')
merchant1 = pd.read_csv('characterEngineer/merchant1_feature.csv')
user1 = pd.read_csv('characterEngineer/user1_feature.csv')
user_merchant1 = pd.read_csv('characterEngineer/user_merchant1_feature.csv')
other_feature1 = pd.read_csv('characterEngineer/other_feature1.csv')

dataset1 = pd.merge(coupon1,other_feature1,on=['User_id','Merchant_id','Coupon_id','Date_received'],how='left')
dataset1 = pd.merge(dataset1,merchant1,on='Merchant_id',how='left')
dataset1 = pd.merge(dataset1,user1,on='User_id',how='left')
dataset1 = pd.merge(dataset1,user_merchant1,on=['User_id','Merchant_id'],how='left')
dataset1.drop_duplicates(inplace=True)
print(dataset1.shape,dataset1.columns.values.tolist())

dataset1.user_merchant_sales_count  = dataset1.user_merchant_sales_count .replace(np.nan,0)
dataset1.user_same_merchant_coupon_counts = dataset1.user_same_merchant_coupon_counts.replace(np.nan,0)
dataset1.diff_merchant_count = dataset1.diff_merchant_count.replace(np.nan,0)
dataset1['is_weekend'] = dataset1.day_of_week.apply(lambda x:1 if x in (6,7) else 0)
weekday_dummies = pd.get_dummies(dataset1.day_of_week)
weekday_dummies.columns = ['weekday'+str(i+1) for i in range(weekday_dummies.shape[1])]
dataset1 = pd.concat([dataset1,weekday_dummies],axis=1)
dataset1 = dataset1.replace(np.nan,"null")
dataset1['label'] = dataset1.Date.astype('str') + ':' + dataset1.Date_received.astype('str')
dataset1.label = dataset1.label.apply(get_label)
dataset1.drop(['Merchant_id','day_of_week','Date','Date_received','Coupon_id','coupon_count'],axis=1,inplace=True)
dataset1 = dataset1.replace('null',np.nan)
print("dataset1:",dataset1.shape)
dataset1.to_csv('data/dataset1.csv', index=None)