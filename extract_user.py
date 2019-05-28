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

# # # # # # # # # # # 提取用户相关特征 # # # # # # # # # # # # # # # # # # #
"""
    user_related:  14个
        count_merchant. 
        user_mean_distance, user_min_distance,user_max_distance,user_median_distance.
        buy_use_coupon. 
        buy_total. 
        coupon_received.
        user_date_datereceived_gap/max_user_date_datereceived_gap/min_user_date_datereceived_gap/avg_user_date_datereceived_gap
        buy_use_coupon_rate = buy_use_coupon/buy_total
        user_coupon_transfer_rate = buy_use_coupon/coupon_received.
"""


def get_user_date_datereceived_gap(s):
    s = s.split(':')
    return (date.date(int(s[0][0:4]),int(s[0][4:6]),int(s[0][6:8])) - date.date(int(s[1][0:4]),int(s[1][4:6]),int(s[1][6:8]))).days

# for feature3
user3 = feature3[['User_id','Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']]

c = user3[['User_id']]
c.drop_duplicates(inplace=True)

c1 = user3[user3.Date!=None][['User_id','Merchant_id']]
c1.drop_duplicates(inplace=True)
c1.Merchant_id = 1
c1 = c1.groupby('User_id').agg('sum').reset_index()
c1.rename(columns={'Merchant_id':'count_merchant'},inplace=True)

c2 = user3[(user3.Date!=None)&(user3.Coupon_id!=None)][['User_id','Distance']]
c2.replace('null', -1, inplace=True)
c2.replace(np.nan,-1,inplace=True)
c2.replace(np.inf,0, inplace=True)
c2.Distance = c2.Distance.astype('int')
c2.replace(-1,np.nan,inplace=True)
c3 = c2.groupby('User_id').agg('min').reset_index()
c3.rename(columns={'Distance':'user_min_distance'},inplace=True)

c4 = c2.groupby('User_id').agg('max').reset_index()
c4.rename(columns={'Distance':'user_max_distance'},inplace=True)

c5 = c2.groupby('User_id').agg('mean').reset_index()
c5.rename(columns={'Distance':'user_mean_distance'},inplace=True)

c6 = c2.groupby('User_id').agg('median').reset_index()
c6.rename(columns={'Distance':'user_median_distance'},inplace=True)

c7 = user3[(user3.Date!=None)&(user3.Coupon_id!=None)][['User_id']]
c7['buy_use_coupon'] = 1
c7 = c7.groupby('User_id').agg('sum').reset_index()

c8 = user3[user3.Date!=None][['User_id']]
c8['buy_total'] = 1
c8 = c8.groupby('User_id').agg('sum').reset_index()

c9 = user3[user3.Coupon_id!=None][['User_id']]
c9['coupon_received'] = 1
c9 = c9.groupby('User_id').agg('sum').reset_index()

c10 = user3[(user3.Date_received!=None )&(user3.Date!=None)][['User_id','Date_received','Date']]
c10.dropna(inplace=True)
c10['Date'] = c10['Date'].astype(str)
c10['Date_received'] = c10['Date_received'].astype(str)
c10['user_date_datereceived_gap'] = c10['Date'] + ":" + c10['Date_received'].apply(str)
c10.user_date_datereceived_gap = c10.user_date_datereceived_gap.apply(get_user_date_datereceived_gap)
c10 = c10[['User_id','user_date_datereceived_gap']]

c11 = c10.groupby('User_id').agg('mean').reset_index()
c11.rename(columns={'user_date_datereceived_gap':'avg_user_date_datereceived_gap'},inplace=True)
c12 = c10.groupby('User_id').agg('min').reset_index()
c12.rename(columns={'user_date_datereceived_gap':'min_user_date_datereceived_gap'},inplace=True)
c13 = c10.groupby('User_id').agg('max').reset_index()
c13.rename(columns={'user_date_datereceived_gap':'max_user_date_datereceived_gap'},inplace=True)

user3_feature = pd.merge(c,c1,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c3,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c4,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c5,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c6,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c7,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c8,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c9,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c11,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c12,on='User_id',how='left')
user3_feature = pd.merge(user3_feature,c13,on='User_id',how='left')
user3_feature.count_merchant = user3_feature.count_merchant.replace(np.nan,0)
user3_feature.buy_use_coupon = user3_feature.buy_use_coupon.replace(np.nan,0)
user3_feature['buy_use_coupon_rate'] = user3_feature.buy_use_coupon.astype('float') / user3_feature.buy_total.astype('float')
user3_feature['user_coupon_transfer_rate'] = user3_feature.buy_use_coupon.astype('float') / user3_feature.coupon_received.astype('float')
user3_feature.buy_total = user3_feature.buy_total.replace(np.nan,0)
user3_feature.coupon_received = user3_feature.coupon_received.replace(np.nan,0)
user3_feature.to_csv('characterEngineer/user3_feature.csv',index=None)

# for feature2
user2 = feature2[['User_id','Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']]

c = user2[['User_id']]
c.drop_duplicates(inplace=True)

c1 = user2[user2.Date!=None][['User_id','Merchant_id']]
c1.drop_duplicates(inplace=True)
c1.Merchant_id = 1
c1 = c1.groupby('User_id').agg('sum').reset_index()
c1.rename(columns={'Merchant_id':'count_merchant'},inplace=True)

c2 = user2[(user2.Date!=None)&(user2.Coupon_id!=None)][['User_id','Distance']]
c2.replace('null',-1,inplace=True)
c2.replace(np.nan,-1,inplace=True)
c2.replace(np.inf,0,inplace=True)
c2.Distance = c2.Distance.astype('int')
c2.replace(-1,np.nan,inplace=True)
c3 = c2.groupby('User_id').agg('min').reset_index()
c3.rename(columns={'Distance':'user_min_distance'},inplace=True)

c4 = c2.groupby('User_id').agg('max').reset_index()
c4.rename(columns={'Distance':'user_max_distance'},inplace=True)

c5 = c2.groupby('User_id').agg('mean').reset_index()
c5.rename(columns={'Distance':'user_mean_distance'},inplace=True)

c6 = c2.groupby('User_id').agg('median').reset_index()
c6.rename(columns={'Distance':'user_median_distance'},inplace=True)

c7 = user2[(user2.Date!=None)&(user2.Coupon_id!=None)][['User_id']]
c7['buy_use_coupon'] = 1
c7 = c7.groupby('User_id').agg('sum').reset_index()

c8 = user2[user2.Date!=None][['User_id']]
c8['buy_total'] = 1
c8 = c8.groupby('User_id').agg('sum').reset_index()

c9 = user2[user2.Coupon_id!=None][['User_id']]
c9['coupon_received'] = 1
c9 = c9.groupby('User_id').agg('sum').reset_index()

c10 = user2[(user2.Date_received!=None)&(user2.Date!=None)][['User_id','Date_received','Date']]
c10.dropna(inplace=True)
c10['Date'] = c10['Date'].astype(str)
c10['Date_received'] = c10['Date_received'].astype(str)
c10['user_date_datereceived_gap'] = c10.Date + ':' + c10.Date_received
c10.user_date_datereceived_gap = c10.user_date_datereceived_gap.apply(get_user_date_datereceived_gap)
c10 = c10[['User_id','user_date_datereceived_gap']]

c11 = c10.groupby('User_id').agg('mean').reset_index()
c11.rename(columns={'user_date_datereceived_gap':'avg_user_date_datereceived_gap'},inplace=True)
c12 = c10.groupby('User_id').agg('min').reset_index()
c12.rename(columns={'user_date_datereceived_gap':'min_user_date_datereceived_gap'},inplace=True)
c13 = c10.groupby('User_id').agg('max').reset_index()
c13.rename(columns={'user_date_datereceived_gap':'max_user_date_datereceived_gap'},inplace=True)

user2_feature = pd.merge(c,c1,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c3,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c4,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c5,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c6,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c7,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c8,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c9,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c11,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c12,on='User_id',how='left')
user2_feature = pd.merge(user2_feature,c13,on='User_id',how='left')
user2_feature.count_merchant = user2_feature.count_merchant.replace(np.nan,0)
user2_feature.buy_use_coupon = user2_feature.buy_use_coupon.replace(np.nan,0)
user2_feature['buy_use_coupon_rate'] = user2_feature.buy_use_coupon.astype('float') / user2_feature.buy_total.astype('float')
user2_feature['user_coupon_transfer_rate'] = user2_feature.buy_use_coupon.astype('float') / user2_feature.coupon_received.astype('float')
user2_feature.buy_total = user2_feature.buy_total.replace(np.nan,0)
user2_feature.coupon_received = user2_feature.coupon_received.replace(np.nan,0)
user2_feature.to_csv('characterEngineer/user2_feature.csv',index=None)

# for feature1
user1 = feature1[['User_id','Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']]

c = user1[['User_id']]
c.drop_duplicates(inplace=True)

c1 = user1[user1.Date!=None][['User_id','Merchant_id']]
c1.drop_duplicates(inplace=True)
c1.Merchant_id = 1
c1 = c1.groupby('User_id').agg('sum').reset_index()
c1.rename(columns={'Merchant_id':'count_merchant'},inplace=True)

c2 = user1[(user1.Date!=None)&(user1.Coupon_id!=None)][['User_id','Distance']]
c2.replace('null',-1,inplace=True)
c2.replace(np.nan,-1,inplace=True)
c2.replace(np.inf,0,inplace=True)

c2.Distance = c2.Distance.astype('int')
c2.replace(-1,np.nan,inplace=True)
c3 = c2.groupby('User_id').agg('min').reset_index()
c3.rename(columns={'Distance':'user_min_distance'},inplace=True)

c4 = c2.groupby('User_id').agg('max').reset_index()
c4.rename(columns={'Distance':'user_max_distance'},inplace=True)

c5 = c2.groupby('User_id').agg('mean').reset_index()
c5.rename(columns={'Distance':'user_mean_distance'},inplace=True)

c6 = c2.groupby('User_id').agg('median').reset_index()
c6.rename(columns={'Distance':'user_median_distance'},inplace=True)

c7 = user1[(user1.Date!=None)&(user1.Coupon_id!=None)][['User_id']]
c7['buy_use_coupon'] = 1
c7 = c7.groupby('User_id').agg('sum').reset_index()

c8 = user1[user1.Date!=None][['User_id']]
c8['buy_total'] = 1
c8 = c8.groupby('User_id').agg('sum').reset_index()

c9 = user1[user1.Coupon_id!=None][['User_id']]
c9['coupon_received'] = 1
c9 = c9.groupby('User_id').agg('sum').reset_index()

c10 = user1[(user1.Date_received!=None)&(user1.Date!=None)][['User_id','Date_received','Date']]


c10.dropna(inplace=True)
c10['Date'] = c10['Date'].astype(str)
c10['Date_received'] = c10['Date_received'].astype(str)
c10['user_date_datereceived_gap'] = c10.Date + ':' + c10.Date_received

c10.user_date_datereceived_gap = c10.user_date_datereceived_gap.apply(get_user_date_datereceived_gap)
c10 = c10[['User_id','user_date_datereceived_gap']]

c11 = c10.groupby('User_id').agg('mean').reset_index()
c11.rename(columns={'user_date_datereceived_gap':'avg_user_date_datereceived_gap'},inplace=True)
c12 = c10.groupby('User_id').agg('min').reset_index()
c12.rename(columns={'user_date_datereceived_gap':'min_user_date_datereceived_gap'},inplace=True)
c13 = c10.groupby('User_id').agg('max').reset_index()
c13.rename(columns={'user_date_datereceived_gap':'max_user_date_datereceived_gap'},inplace=True)

user1_feature = pd.merge(c,c1,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c3,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c4,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c5,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c6,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c7,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c8,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c9,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c11,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c12,on='User_id',how='left')
user1_feature = pd.merge(user1_feature,c13,on='User_id',how='left')
user1_feature.count_merchant = user1_feature.count_merchant.replace(np.nan,0)
user1_feature.buy_use_coupon = user1_feature.buy_use_coupon.replace(np.nan,0)
user1_feature['buy_use_coupon_rate'] = user1_feature.buy_use_coupon.astype('float') / user1_feature.buy_total.astype('float')
user1_feature['user_coupon_transfer_rate'] = user1_feature.buy_use_coupon.astype('float') / user1_feature.coupon_received.astype('float')
user1_feature.buy_total = user1_feature.buy_total.replace(np.nan,0)
user1_feature.coupon_received = user1_feature.coupon_received.replace(np.nan,0)
print(user1_feature.shape)
user1_feature.to_csv('characterEngineer/user1_feature.csv',index=None)