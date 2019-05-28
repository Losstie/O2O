#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file:extract_user.py
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

# # # # # # # # # # # # # # # # # 提取商家-用户交互特征 # # # # # # # # # # # # # # # # # # # # #
"""
user_merchant_interaction:10个特征
    user_merchant_received_coupon_count
    user_merchant_sales_count
    user_merchant_usecoupon_sales_count
    user_merchant_receivedcoupon_notuse_count = user_merchant_received_coupon_count - user_merchant_usecoupon_sales_count
    user_merchant_usecoupon_sales_rate = user_merchant_usecoupon_sales_count /user_merchant_received_coupon_count
    user_merchant_coupon_transfer_rate = user_merchant_usecoupon_sales_count / user_merchant_sales_count
    user_merchant_foruser_received_coupon_notuse_rate = user_merchant_receivedcoupon_notuse_count / user_received_coupon_notuse_count
    user_merchant_foruser_received_coupon_use_rate = user_merchant_usecoupon_sales_count / user_received_coupon_use_count
    user_merchant_formerchant_received_coupon_notuse_rate = user_merchant_receivedcoupon_notuse_count / merchant_coupon_notuse_count
    user_merchant_formerchant_received_coupon_use_rate = user_merchant_usecoupon_sales_count / merchant_coupon_used_count

"""

# for feature3
c = feature3[['User_id', 'Merchant_id', 'Coupon_id', 'Date_received', 'Date']]

c1 = c[['User_id', 'Merchant_id', 'Coupon_id']]
c1 = c1[c1.Coupon_id != None]
c1['user_merchant_received_coupon_count'] = 1
c1 = c1.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()

c2 = c[['User_id', 'Merchant_id', 'Date']]
c2 = c2[c2.Date != None]
c2['user_merchant_sales_count'] = 1
c2 = c2.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()
user_merchant3_feature = pd.merge(c1, c2, on=['User_id', 'Merchant_id'])

c3 = c[['User_id', 'Merchant_id', 'Coupon_id', 'Date']]
c3 = c3[(c3.Coupon_id != None) & (c3.Date != None)]
c3 = c3[['User_id', 'Merchant_id']]
c3['user_merchant_usecoupon_sales_count'] = 1
c3 = c3.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()
user_merchant3_feature = pd.merge(user_merchant3_feature, c3, on=['User_id', 'Merchant_id'], how='left')
user_merchant3_feature.user_merchant_sales_count = user_merchant3_feature.user_merchant_sales_count.replace(np.nan, 0)
user_merchant3_feature.user_merchant_usecoupon_sales_count = user_merchant3_feature.user_merchant_usecoupon_sales_count.replace(
    np.nan, 0)
user_merchant3_feature[
    'user_merchant_receivedcoupon_notuse_count'] = user_merchant3_feature.user_merchant_received_coupon_count - user_merchant3_feature.user_merchant_usecoupon_sales_count
user_merchant3_feature[
    'user_merchant_usecoupon_sales_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.user_merchant_received_coupon_count
user_merchant3_feature[
    'user_merchant_coupon_transfer_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.user_merchant_sales_count
user_merchant3_feature.user_merchant_coupon_transfer_rate = user_merchant3_feature.user_merchant_coupon_transfer_rate.replace(
    np.nan, 0)

c4 = c[['User_id', 'Coupon_id']]
c4 = c4[c4.Coupon_id != None]
c4['user_received_coupon_count'] = 1
c4 = c4.groupby('User_id').agg('sum').reset_index()

c5 = c[['User_id', 'Coupon_id', 'Date']]
c5 = c5[(c5.Coupon_id != None) & (c5.Date != None)]
c5 = c5[['User_id']]
c5['user_received_coupon_use_count'] = 1
c5 = c5.groupby(['User_id']).agg('sum').reset_index()
c5 = pd.merge(c4, c5, on=['User_id']).reset_index()
c5.user_received_coupon_use_count = c5.user_received_coupon_use_count.replace(np.nan, 0)
c5['user_received_coupon_notuse_count'] = c5.user_received_coupon_count - c5.user_received_coupon_use_count
c5 = c5[['User_id', 'user_received_coupon_use_count', 'user_received_coupon_notuse_count']]

c6 = c[['Merchant_id', 'Coupon_id']]
c6 = c6[c6.Coupon_id != None]
c6 = c6[['Merchant_id']]
c6['merchant_coupon_sum'] = 1
c6 = c6.groupby(['Merchant_id']).agg('sum').reset_index()

c7 = c[['Merchant_id', 'Coupon_id', 'Date']]
c7 = c7[(c7.Coupon_id != None) & (c7.Date != None)]
c7 = c7[['Merchant_id']]
c7['merchant_coupon_used_count'] = 1
c7 = c7.groupby(['Merchant_id']).agg('sum').reset_index()
c7 = pd.merge(c6, c7, on=['Merchant_id']).reset_index()
c7.merchant_coupon_used_count = c7.merchant_coupon_used_count.replace(np.nan, 0)
c7['merchant_coupon_notuse_count'] = c7.merchant_coupon_sum - c7.merchant_coupon_used_count
c7 = c7[['Merchant_id', 'merchant_coupon_used_count', 'merchant_coupon_notuse_count']]

user_merchant3_feature = pd.merge(user_merchant3_feature, c7, on=['Merchant_id'], how='left')
user_merchant3_feature.merchant_coupon_used_count = user_merchant3_feature.merchant_coupon_used_count.replace(np.nan, 0)
user_merchant3_feature.merchant_coupon_notuse_count = user_merchant3_feature.merchant_coupon_notuse_count.replace(
    np.nan, 0)
user_merchant3_feature = pd.merge(user_merchant3_feature, c5, on=['User_id'], how='left')
user_merchant3_feature.user_received_coupon_use_count = user_merchant3_feature.user_received_coupon_use_count.replace(
    np.nan, 0)
user_merchant3_feature.user_received_coupon_notuse_count = user_merchant3_feature.user_received_coupon_notuse_count.replace(
    np.nan, 0)
user_merchant3_feature[
    'user_merchant_foruser_received_coupon_notuse_rate'] = 1.0 * user_merchant3_feature.user_merchant_receivedcoupon_notuse_count / user_merchant3_feature.user_received_coupon_notuse_count
user_merchant3_feature[
    'user_merchant_foruser_received_coupon_use_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.user_received_coupon_use_count
user_merchant3_feature[
    'user_merchant_formerchant_received_coupon_notuse_rate'] = 1.0 * user_merchant3_feature.user_merchant_receivedcoupon_notuse_count / user_merchant3_feature.merchant_coupon_notuse_count
user_merchant3_feature[
    'user_merchant_formerchant_received_coupon_use_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.merchant_coupon_used_count
user_merchant3_feature = user_merchant3_feature[
    ['User_id', 'Merchant_id', 'user_merchant_received_coupon_count', 'user_merchant_sales_count',
     'user_merchant_usecoupon_sales_count', 'user_merchant_receivedcoupon_notuse_count',
     'user_merchant_usecoupon_sales_rate', 'user_merchant_coupon_transfer_rate',
     'user_merchant_foruser_received_coupon_notuse_rate', 'user_merchant_foruser_received_coupon_use_rate',
     'user_merchant_formerchant_received_coupon_notuse_rate', 'user_merchant_formerchant_received_coupon_use_rate']]
user_merchant3_feature.to_csv('characterEngineer/user_merchant3_feature.csv',index=None)
print(user_merchant3_feature.shape)

# for feature2
c = feature2[['User_id', 'Merchant_id', 'Coupon_id', 'Date_received', 'Date']]

c1 = c[['User_id', 'Merchant_id', 'Coupon_id']]
c1 = c1[c1.Coupon_id != None]
c1['user_merchant_received_coupon_count'] = 1
c1 = c1.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()

c2 = c[['User_id', 'Merchant_id', 'Date']]
c2 = c2[c2.Date != None]
c2['user_merchant_sales_count'] = 1
c2 = c2.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()
user_merchant2_feature = pd.merge(c1, c2, on=['User_id', 'Merchant_id'])

c3 = c[['User_id', 'Merchant_id', 'Coupon_id', 'Date']]
c3 = c3[(c3.Coupon_id != None) & (c3.Date != None)]
c3 = c3[['User_id', 'Merchant_id']]
c3['user_merchant_usecoupon_sales_count'] = 1
c3 = c3.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()
user_merchant2_feature = pd.merge(user_merchant2_feature, c3, on=['User_id', 'Merchant_id'], how='left')
user_merchant2_feature.user_merchant_sales_count = user_merchant2_feature.user_merchant_sales_count.replace(np.nan, 0)
user_merchant2_feature.user_merchant_usecoupon_sales_count = user_merchant2_feature.user_merchant_usecoupon_sales_count.replace(
    np.nan, 0)
user_merchant2_feature[
    'user_merchant_receivedcoupon_notuse_count'] = user_merchant2_feature.user_merchant_received_coupon_count - user_merchant2_feature.user_merchant_usecoupon_sales_count
user_merchant2_feature[
    'user_merchant_usecoupon_sales_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.user_merchant_received_coupon_count
user_merchant2_feature[
    'user_merchant_coupon_transfer_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.user_merchant_sales_count
user_merchant2_feature.user_merchant_coupon_transfer_rate = user_merchant2_feature.user_merchant_coupon_transfer_rate.replace(
    np.nan, 0)

c4 = c[['User_id', 'Coupon_id']]
c4 = c4[c4.Coupon_id != None]
c4['user_received_coupon_count'] = 1
c4 = c4.groupby('User_id').agg('sum').reset_index()

c5 = c[['User_id', 'Coupon_id', 'Date']]
c5 = c5[(c5.Coupon_id != None) & (c5.Date != None)]
c5 = c5[['User_id']]
c5['user_received_coupon_use_count'] = 1
c5 = c5.groupby(['User_id']).agg('sum').reset_index()
c5 = pd.merge(c4, c5, on=['User_id']).reset_index()
c5.user_received_coupon_use_count = c5.user_received_coupon_use_count.replace(np.nan, 0)
c5['user_received_coupon_notuse_count'] = c5.user_received_coupon_count - c5.user_received_coupon_use_count
c5 = c5[['User_id', 'user_received_coupon_use_count', 'user_received_coupon_notuse_count']]

c6 = c[['Merchant_id', 'Coupon_id']]
c6 = c6[c6.Coupon_id != None]
c6 = c6[['Merchant_id']]
c6['merchant_coupon_sum'] = 1
c6 = c6.groupby(['Merchant_id']).agg('sum').reset_index()

c7 = c[['Merchant_id', 'Coupon_id', 'Date']]
c7 = c7[(c7.Coupon_id != None) & (c7.Date != None)]
c7 = c7[['Merchant_id']]
c7['merchant_coupon_used_count'] = 1
c7 = c7.groupby(['Merchant_id']).agg('sum').reset_index()
c7 = pd.merge(c6, c7, on=['Merchant_id']).reset_index()
c7.merchant_coupon_used_count = c7.merchant_coupon_used_count.replace(np.nan, 0)
c7['merchant_coupon_notuse_count'] = c7.merchant_coupon_sum - c7.merchant_coupon_used_count
c7 = c7[['Merchant_id', 'merchant_coupon_used_count', 'merchant_coupon_notuse_count']]

user_merchant2_feature = pd.merge(user_merchant2_feature, c7, on=['Merchant_id'], how='left')
user_merchant2_feature.merchant_coupon_used_count = user_merchant2_feature.merchant_coupon_used_count.replace(np.nan, 0)
user_merchant2_feature.merchant_coupon_notuse_count = user_merchant2_feature.merchant_coupon_notuse_count.replace(
    np.nan, 0)
user_merchant2_feature = pd.merge(user_merchant2_feature, c5, on=['User_id'], how='left')
user_merchant2_feature.user_received_coupon_use_count = user_merchant2_feature.user_received_coupon_use_count.replace(
    np.nan, 0)
user_merchant2_feature.user_received_coupon_notuse_count = user_merchant2_feature.user_received_coupon_notuse_count.replace(
    np.nan, 0)
user_merchant2_feature[
    'user_merchant_foruser_received_coupon_notuse_rate'] = 1.0 * user_merchant2_feature.user_merchant_receivedcoupon_notuse_count / user_merchant2_feature.user_received_coupon_notuse_count
user_merchant2_feature[
    'user_merchant_foruser_received_coupon_use_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.user_received_coupon_use_count
user_merchant2_feature[
    'user_merchant_formerchant_received_coupon_notuse_rate'] = 1.0 * user_merchant2_feature.user_merchant_receivedcoupon_notuse_count / user_merchant2_feature.merchant_coupon_notuse_count
user_merchant2_feature[
    'user_merchant_formerchant_received_coupon_use_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.merchant_coupon_used_count
user_merchant2_feature = user_merchant2_feature[
    ['User_id', 'Merchant_id', 'user_merchant_received_coupon_count', 'user_merchant_sales_count',
     'user_merchant_usecoupon_sales_count', 'user_merchant_receivedcoupon_notuse_count',
     'user_merchant_usecoupon_sales_rate', 'user_merchant_coupon_transfer_rate',
     'user_merchant_foruser_received_coupon_notuse_rate', 'user_merchant_foruser_received_coupon_use_rate',
     'user_merchant_formerchant_received_coupon_notuse_rate', 'user_merchant_formerchant_received_coupon_use_rate']]
user_merchant2_feature.to_csv('characterEngineer/user_merchant2_feature.csv',index=None)
print(user_merchant2_feature.shape)

# for feature1
c = feature1[['User_id', 'Merchant_id', 'Coupon_id', 'Date_received', 'Date']]

c1 = c[['User_id', 'Merchant_id', 'Coupon_id']]
c1 = c1[c1.Coupon_id != None]
c1['user_merchant_received_coupon_count'] = 1
c1 = c1.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()

c2 = c[['User_id', 'Merchant_id', 'Date']]
c2 = c2[c2.Date != None]
c2['user_merchant_sales_count'] = 1
c2 = c2.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()
user_merchant1_feature = pd.merge(c1, c2, on=['User_id', 'Merchant_id'])

c3 = c[['User_id', 'Merchant_id', 'Coupon_id', 'Date']]
c3 = c3[(c3.Coupon_id != None) & (c3.Date != None)]
c3 = c3[['User_id', 'Merchant_id']]
c3['user_merchant_usecoupon_sales_count'] = 1
c3 = c3.groupby(['User_id', 'Merchant_id']).agg('sum').reset_index()
user_merchant1_feature = pd.merge(user_merchant1_feature, c3, on=['User_id', 'Merchant_id'], how='left')
user_merchant1_feature.user_merchant_sales_count = user_merchant1_feature.user_merchant_sales_count.replace(np.nan, 0)
user_merchant1_feature.user_merchant_usecoupon_sales_count = user_merchant1_feature.user_merchant_usecoupon_sales_count.replace(
    np.nan, 0)
user_merchant1_feature[
    'user_merchant_receivedcoupon_notuse_count'] = user_merchant1_feature.user_merchant_received_coupon_count - user_merchant1_feature.user_merchant_usecoupon_sales_count
user_merchant1_feature[
    'user_merchant_usecoupon_sales_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.user_merchant_received_coupon_count
user_merchant1_feature[
    'user_merchant_coupon_transfer_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.user_merchant_sales_count
user_merchant1_feature.user_merchant_coupon_transfer_rate = user_merchant1_feature.user_merchant_coupon_transfer_rate.replace(
    np.nan, 0)

c4 = c[['User_id', 'Coupon_id']]
c4 = c4[c4.Coupon_id != None]
c4['user_received_coupon_count'] = 1
c4 = c4.groupby('User_id').agg('sum').reset_index()

c5 = c[['User_id', 'Coupon_id', 'Date']]
c5 = c5[(c5.Coupon_id != None) & (c5.Date != None)]
c5 = c5[['User_id']]
c5['user_received_coupon_use_count'] = 1
c5 = c5.groupby(['User_id']).agg('sum').reset_index()
c5 = pd.merge(c4, c5, on=['User_id']).reset_index()
c5.user_received_coupon_use_count = c5.user_received_coupon_use_count.replace(np.nan, 0)
c5['user_received_coupon_notuse_count'] = c5.user_received_coupon_count - c5.user_received_coupon_use_count
c5 = c5[['User_id', 'user_received_coupon_use_count', 'user_received_coupon_notuse_count']]

c6 = c[['Merchant_id', 'Coupon_id']]
c6 = c6[c6.Coupon_id != None]
c6 = c6[['Merchant_id']]
c6['merchant_coupon_sum'] = 1
c6 = c6.groupby(['Merchant_id']).agg('sum').reset_index()

c7 = c[['Merchant_id', 'Coupon_id', 'Date']]
c7 = c7[(c7.Coupon_id != None) & (c7.Date != None)]
c7 = c7[['Merchant_id']]
c7['merchant_coupon_used_count'] = 1
c7 = c7.groupby(['Merchant_id']).agg('sum').reset_index()
c7 = pd.merge(c6, c7, on=['Merchant_id']).reset_index()
c7.merchant_coupon_used_count = c7.merchant_coupon_used_count.replace(np.nan, 0)
c7['merchant_coupon_notuse_count'] = c7.merchant_coupon_sum - c7.merchant_coupon_used_count
c7 = c7[['Merchant_id', 'merchant_coupon_used_count', 'merchant_coupon_notuse_count']]

user_merchant1_feature = pd.merge(user_merchant1_feature, c7, on=['Merchant_id'], how='left')
user_merchant1_feature.merchant_coupon_used_count = user_merchant1_feature.merchant_coupon_used_count.replace(np.nan, 0)
user_merchant1_feature.merchant_coupon_notuse_count = user_merchant1_feature.merchant_coupon_notuse_count.replace(
    np.nan, 0)
user_merchant1_feature = pd.merge(user_merchant1_feature, c5, on=['User_id'], how='left')
user_merchant1_feature.user_received_coupon_use_count = user_merchant1_feature.user_received_coupon_use_count.replace(
    np.nan, 0)
user_merchant1_feature.user_received_coupon_notuse_count = user_merchant1_feature.user_received_coupon_notuse_count.replace(
    np.nan, 0)
user_merchant1_feature[
    'user_merchant_foruser_received_coupon_notuse_rate'] = 1.0 * user_merchant1_feature.user_merchant_receivedcoupon_notuse_count / user_merchant1_feature.user_received_coupon_notuse_count
user_merchant1_feature[
    'user_merchant_foruser_received_coupon_use_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.user_received_coupon_use_count
user_merchant1_feature[
    'user_merchant_formerchant_received_coupon_notuse_rate'] = 1.0 * user_merchant1_feature.user_merchant_receivedcoupon_notuse_count / user_merchant1_feature.merchant_coupon_notuse_count
user_merchant1_feature[
    'user_merchant_formerchant_received_coupon_use_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.merchant_coupon_used_count
user_merchant1_feature = user_merchant1_feature[
    ['User_id', 'Merchant_id', 'user_merchant_received_coupon_count', 'user_merchant_sales_count',
     'user_merchant_usecoupon_sales_count', 'user_merchant_receivedcoupon_notuse_count',
     'user_merchant_usecoupon_sales_rate', 'user_merchant_coupon_transfer_rate',
     'user_merchant_foruser_received_coupon_notuse_rate', 'user_merchant_foruser_received_coupon_use_rate',
     'user_merchant_formerchant_received_coupon_notuse_rate', 'user_merchant_formerchant_received_coupon_use_rate']]
user_merchant1_feature.to_csv('characterEngineer/user_merchant1_feature.csv',index=None)
print(user_merchant1_feature.shape)
