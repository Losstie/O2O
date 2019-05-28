#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file:extract_merchant.py
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

# # # # # # # # # # # 提取商家相关特征 # # # # # # # # # # # # # # # # # # #
"""
merchant related: 9个
      1.total_sales 2.sales_use_coupon.  3.total_coupon
      4.coupon_rate = sales_use_coupon/total_sales.  
      5.merchant_coupon_transfer_rate = sales_use_coupon/total_coupon. 
      6.merchant_median_distance 7.merchant_mean_distance 8.merchant_min_distance 9.merchant_max_distance
"""


# for feature3
merchant3 = feature3[['Merchant_id','Coupon_id','Distance','Date_received','Date']]
c = merchant3[['Merchant_id']]
c.drop_duplicates(inplace=True)

c1 = merchant3[merchant3.Date!=None][['Merchant_id']]
c1['total_sales'] = 1
c1 = c1.groupby('Merchant_id').agg('sum').reset_index()

c2 = merchant3[(merchant3.Date!=None)&(merchant3.Coupon_id!=None)][['Merchant_id']]
c2['sales_use_coupon'] = 1
c2 = c2.groupby('Merchant_id').agg('sum').reset_index()

c3 = merchant3[merchant3.Coupon_id!=None][['Merchant_id']]
c3['total_coupon'] = 1
c3 = c3.groupby('Merchant_id').agg('sum').reset_index()

c4 = merchant3[(merchant3.Date!=None)&(merchant3.Coupon_id!=None)][['Merchant_id','Distance']]
c4.replace('null',-1,inplace=True)
c4.Distance = c4.Distance.astype(np.float32)
c4.replace(-1,np.nan,inplace=True)
c5 = c4.groupby('Merchant_id').agg('min').reset_index()
c5.rename(columns={'Distance':'merchant_min_distance'},inplace=True)

c6 = c4.groupby('Merchant_id').agg('max').reset_index()
c6.rename(columns={'Distance':'merchant_max_distance'},inplace=True)

c7 = c4.groupby('Merchant_id').agg('mean').reset_index()
c7.rename(columns={'Distance':'merchant_mean_distance'},inplace=True)

c8 = c4.groupby('Merchant_id').agg('median').reset_index()
c8.rename(columns={'Distance':'merchant_median_distance'},inplace=True)

merchant3_feature = pd.merge(c,c1,on='Merchant_id',how='left')
merchant3_feature = pd.merge(merchant3_feature,c2,on='Merchant_id',how='left')
merchant3_feature = pd.merge(merchant3_feature,c3,on='Merchant_id',how='left')
merchant3_feature = pd.merge(merchant3_feature,c5,on='Merchant_id',how='left')
merchant3_feature = pd.merge(merchant3_feature,c6,on='Merchant_id',how='left')
merchant3_feature = pd.merge(merchant3_feature,c7,on='Merchant_id',how='left')
merchant3_feature = pd.merge(merchant3_feature,c8,on='Merchant_id',how='left')
merchant3_feature.sales_use_coupon = merchant3_feature.sales_use_coupon.replace(np.nan,0) #fillna with 0
merchant3_feature['merchant_coupon_transfer_rate'] = merchant3_feature.sales_use_coupon.astype(np.float32) / merchant3_feature.total_coupon
merchant3_feature['coupon_rate'] = merchant3_feature.sales_use_coupon.astype(np.float32) / merchant3_feature.total_sales
merchant3_feature.total_coupon = merchant3_feature.total_coupon.replace(np.nan,0) #fillna with 0
merchant3_feature.to_csv('characterEngineer/merchant3_feature.csv',index=None)
print(merchant3_feature.shape)

# for feature2
merchant2 = feature2[['Merchant_id','Coupon_id','Distance','Date_received','Date']]
c = merchant2[['Merchant_id']]
c.drop_duplicates(inplace=True)

c1 = merchant2[merchant2.Date!=None][['Merchant_id']]
c1['total_sales'] = 1
c1 = c1.groupby('Merchant_id').agg('sum').reset_index()

c2 = merchant2[(merchant2.Date!=None)&(merchant2.Coupon_id!=None)][['Merchant_id']]
c2['sales_use_coupon'] = 1
c2 = c2.groupby('Merchant_id').agg('sum').reset_index()

c3 = merchant2[merchant2.Coupon_id!=None][['Merchant_id']]
c3['total_coupon'] = 1
c3 = c3.groupby('Merchant_id').agg('sum').reset_index()

c4 = merchant2[(merchant2.Date!=None)&(merchant2.Coupon_id!=None)][['Merchant_id','Distance']]
c4.replace('null',-1,inplace=True)
c4.Distance = c4.Distance.astype(np.float32)
c4.replace(-1,np.nan,inplace=True)
c5 = c4.groupby('Merchant_id').agg('min').reset_index()
c5.rename(columns={'Distance':'merchant_min_distance'},inplace=True)

c6 = c4.groupby('Merchant_id').agg('max').reset_index()
c6.rename(columns={'Distance':'merchant_max_distance'},inplace=True)

c7 = c4.groupby('Merchant_id').agg('mean').reset_index()
c7.rename(columns={'Distance':'merchant_mean_distance'},inplace=True)

c8 = c4.groupby('Merchant_id').agg('median').reset_index()
c8.rename(columns={'Distance':'merchant_median_distance'},inplace=True)

merchant2_feature = pd.merge(c,c1,on='Merchant_id',how='left')
merchant2_feature = pd.merge(merchant2_feature,c2,on='Merchant_id',how='left')
merchant2_feature = pd.merge(merchant2_feature,c3,on='Merchant_id',how='left')
merchant2_feature = pd.merge(merchant2_feature,c5,on='Merchant_id',how='left')
merchant2_feature = pd.merge(merchant2_feature,c6,on='Merchant_id',how='left')
merchant2_feature = pd.merge(merchant2_feature,c7,on='Merchant_id',how='left')
merchant2_feature = pd.merge(merchant2_feature,c8,on='Merchant_id',how='left')
merchant2_feature.sales_use_coupon = merchant2_feature.sales_use_coupon.replace(np.nan,0) #fillna with 0
merchant2_feature['merchant_coupon_transfer_rate'] = merchant2_feature.sales_use_coupon.astype(np.float32) / merchant2_feature.total_coupon
merchant2_feature['coupon_rate'] = merchant2_feature.sales_use_coupon.astype(np.float32) / merchant2_feature.total_sales
merchant2_feature.total_coupon = merchant2_feature.total_coupon.replace(np.nan,0) #fillna with 0
merchant2_feature.to_csv('characterEngineer/merchant2_feature.csv',index=None)
print(merchant2_feature.shape)

# for feature1
merchant1 = feature1[['Merchant_id','Coupon_id','Distance','Date_received','Date']]
c = merchant1[['Merchant_id']]
c.drop_duplicates(inplace=True)

c1 = merchant1[merchant1.Date!=None][['Merchant_id']]
c1['total_sales'] = 1
c1 = c1.groupby('Merchant_id').agg('sum').reset_index()

c2 = merchant1[(merchant1.Date!=None)&(merchant1.Coupon_id!=None)][['Merchant_id']]
c2['sales_use_coupon'] = 1
c2 = c2.groupby('Merchant_id').agg('sum').reset_index()

c3 = merchant1[merchant1.Coupon_id!=None][['Merchant_id']]
c3['total_coupon'] = 1
c3 = c3.groupby('Merchant_id').agg('sum').reset_index()

c4 = merchant1[(merchant1.Date!=None)&(merchant1.Coupon_id!=None)][['Merchant_id','Distance']]
c4.replace('null',-1,inplace=True)
c4.Distance = c4.Distance.astype(np.float32)
c4.replace(-1,np.nan,inplace=True)
c5 = c4.groupby('Merchant_id').agg('min').reset_index()
c5.rename(columns={'Distance':'merchant_min_distance'},inplace=True)

c6 = c4.groupby('Merchant_id').agg('max').reset_index()
c6.rename(columns={'Distance':'merchant_max_distance'},inplace=True)

c7 = c4.groupby('Merchant_id').agg('mean').reset_index()
c7.rename(columns={'Distance':'merchant_mean_distance'},inplace=True)

c8 = c4.groupby('Merchant_id').agg('median').reset_index()
c8.rename(columns={'Distance':'merchant_median_distance'},inplace=True)

merchant1_feature = pd.merge(c,c1,on='Merchant_id',how='left')
merchant1_feature = pd.merge(merchant1_feature,c2,on='Merchant_id',how='left')
merchant1_feature = pd.merge(merchant1_feature,c3,on='Merchant_id',how='left')
merchant1_feature = pd.merge(merchant1_feature,c5,on='Merchant_id',how='left')
merchant1_feature = pd.merge(merchant1_feature,c6,on='Merchant_id',how='left')
merchant1_feature = pd.merge(merchant1_feature,c7,on='Merchant_id',how='left')
merchant1_feature = pd.merge(merchant1_feature,c8,on='Merchant_id',how='left')
merchant1_feature.sales_use_coupon = merchant1_feature.sales_use_coupon.replace(np.nan,0) #fillna with 0
merchant1_feature['merchant_coupon_transfer_rate'] = merchant1_feature.sales_use_coupon.astype(np.float32) / merchant1_feature.total_coupon
merchant1_feature['coupon_rate'] = merchant1_feature.sales_use_coupon.astype(np.float32) / merchant1_feature.total_sales
merchant1_feature.total_coupon = merchant1_feature.total_coupon.replace(np.nan,0) #fillna with 0
merchant1_feature.to_csv('characterEngineer/merchant1_feature.csv',index=None)
print(merchant1_feature.shape)