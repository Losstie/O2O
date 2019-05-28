#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file:extract_coupon.py
@author: losstie
@create_time: 2019/5/20 22:13
@description:
"""
import pandas as pd
import numpy as np
import datetime as date

"""
划分数据集  依据：date_reveived
 dateset3: 20160701~20160731 (113640),features3 from 20160315~20160630  (off_test)
 dateset2: 20160515~20160615 (258446),features2 from 20160201~20160514  
 dateset1: 20160414~20160514 (138303),features1 from 20160101~20160413   

"""
# 划分数据集
off_train = pd.read_csv("data/ccf_offline_stage1_train.csv")
online_train = pd.read_csv("data/ccf_online_stage1_train.csv")
off_test = pd.read_csv("data/ccf_offline_stage1_test_revised.csv")
dataset3 = off_test
print(off_train.head())
feature3 = off_train[((off_train.Date>=20160315)&(off_train.Date<=20160630))|((off_train.Date==None)&(off_train.Date_received>=20160315)&(off_train.Date_received<=20160630))]
dataset2 = off_train[(off_train.Date_received>=20160515)&(off_train.Date_received<=20160615)]
feature2 = off_train[(off_train.Date>=20160201)&(off_train.Date<=20160514)|((off_train.Date==None)&(off_train.Date_received>=20160201)&(off_train.Date_received<=20160514))]
dataset1 = off_train[(off_train.Date_received>=20160414)&(off_train.Date_received<=20160514)]
feature1 = off_train[(off_train.Date>=20160101)&(off_train.Date<=20160413)|((off_train.Date==None)&(off_train.Date_received>=20160101)&(off_train.Date_received<=20160413))]

# # # # # # # # # # # 提取优惠券相关特征 # # # # # # # # # # # # # # # # # # #
"""
2.coupon related: 5
      discount_rate. discount_man. discount_jian. is_man_jian
      day_of_week,day_of_month. (date_received)
"""
def calc_discount_rate(s):
    s =str(s)
    s = s.split(':')
    if len(s)==1:
        return float(s[0])
    else:
        return 1.0-float(s[1])/float(s[0])

def get_discount_man(s):
    s =str(s)
    s = s.split(':')
    if len(s)==1:
        return 'null'
    else:
        return int(s[0])

def get_discount_jian(s):
    s =str(s)
    s = s.split(':')
    if len(s)==1:
        return 'null'
    else:
        return int(s[1])

def is_man_jian(s):
    s =str(s)
    s = s.split(':')
    if len(s)==1:
        return 0
    else:
        return 1

#dataset3
dataset3['day_of_week'] = dataset3.Date_received.astype('str').apply(lambda x:date.date(int(x[0:4]),int(x[4:6]),int(x[6:8])).weekday()+1)
dataset3['day_of_month'] = dataset3.Date_received.astype('str').apply(lambda x:int(x[6:8]))
dataset3['days_distance'] = dataset3.Date_received.astype('str').apply(lambda x:(date.date(int(x[0:4]),int(x[4:6]),int(x[6:8]))-date.date(2016,6,30)).days)
dataset3['discount_man'] = dataset3.Discount_rate.apply(get_discount_man)
dataset3['discount_jian'] = dataset3.Discount_rate.apply(get_discount_jian)
dataset3['is_man_jian'] = dataset3.Discount_rate.apply(is_man_jian)
dataset3['Discount_rate'] = dataset3.Discount_rate.apply(calc_discount_rate)
d = dataset3[['Coupon_id']]
d['coupon_count'] = 1
d = d.groupby('Coupon_id').agg('sum').reset_index()
dataset3 = pd.merge(dataset3,d,on='Coupon_id',how='left')
print(dataset3 .shape)
print(dataset3 .columns.values.tolist())
dataset3.to_csv('characterEngineer/coupon3_feature.csv',index=None)
#dataset2
dataset2['day_of_week'] = dataset2.Date_received.astype('str').apply(lambda x:date.date(int(x[0:4]),int(x[4:6]),int(x[6:8])).weekday()+1)
dataset2['day_of_month'] = dataset2.Date_received.astype('str').apply(lambda x:int(x[6:8]))
dataset2['days_distance'] = dataset2.Date_received.astype('str').apply(lambda x:(date.date(int(x[0:4]),int(x[4:6]),int(x[6:8]))-date.date(2016,5,14)).days)
dataset2['discount_man'] = dataset2.Discount_rate.apply(get_discount_man)
dataset2['discount_jian'] = dataset2.Discount_rate.apply(get_discount_jian)
dataset2['is_man_jian'] = dataset2.Discount_rate.apply(is_man_jian)
dataset2['Discount_rate'] = dataset2.Discount_rate.apply(calc_discount_rate)
d = dataset2[['Coupon_id']]
d['coupon_count'] = 1
d = d.groupby('Coupon_id').agg('sum').reset_index()
dataset2 = pd.merge(dataset2,d,on='Coupon_id',how='left')
print(dataset2.shape)
print(dataset2.columns.values.tolist())
dataset2.to_csv('characterEngineer/coupon2_feature.csv',index=None)
#dataset1
dataset1['day_of_week'] = dataset1.Date_received.astype('str').apply(lambda x:date.date(int(x[0:4]),int(x[4:6]),int(x[6:8])).weekday()+1)
dataset1['day_of_month'] = dataset1.Date_received.astype('str').apply(lambda x:int(x[6:8]))
dataset1['days_distance'] = dataset1.Date_received.astype('str').apply(lambda x:(date.date(int(x[0:4]),int(x[4:6]),int(x[6:8]))-date.date(2016,4,13)).days)
dataset1['discount_man'] = dataset1.Discount_rate.apply(get_discount_man)
dataset1['discount_jian'] = dataset1.Discount_rate.apply(get_discount_jian)
dataset1['is_man_jian'] = dataset1.Discount_rate.apply(is_man_jian)
dataset1['Discount_rate'] = dataset1.Discount_rate.apply(calc_discount_rate)
d = dataset1[['Coupon_id']]
d['coupon_count'] = 1
d = d.groupby('Coupon_id').agg('sum').reset_index()
dataset1 = pd.merge(dataset1, d, on='Coupon_id',how='left')
print(dataset1.shape)
print(dataset1.columns.values.tolist())
dataset1.to_csv('characterEngineer/coupon1_feature.csv',index=None)