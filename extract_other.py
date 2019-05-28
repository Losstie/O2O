#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file:extract_other.py
@author: losstie
@create_time: 2019/5/22 9:23
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

# # # # # # # # # # # ##  # # # 提取额外特征 # # # # # # # # # # # # # #
"""
additional feature:19个
1.this_month_user_reveive_count 2.this_month_user_receive_same_coupon_count
3.this_day_user_receive_all_coupon_count 4.this_day_user_receive_same_coupon_count
5.this_month_user_received_same_coupon_isfirstone 6.this_month_user_received_same_coupon_islastone
7.user_this_gap_all_before               8.user_this_gap_all_after
9.day_gap_before/day_gap_afte          10.same_coupon_day_count_before
11.same_coupon_day_count_after          12.user_same_merchant_coupon_counts
13.diff_merchant_count                  14.user_all_diff_coupon_count
15.merchant_coupon_count                16.merchant_same_coupon_count
17.merchant_all_diff_user_count         18.merchant_diff_coupon_count


"""
# for dataset3
other_feature3 = dataset3[['User_id','Merchant_id','Coupon_id','Date_received']]

c = dataset3[['User_id']]
# 该用户该月领取优惠券总数
c.loc[:,'this_month_user_reveive_count'] = 1
c = c.groupby('User_id').agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c,on='User_id')

c1 = dataset3[["User_id","Coupon_id"]]
# 该用户该月领取特定优惠券数目
c1.loc[:,'this_month_user_receive_same_coupon_count'] = 1
c1 = c1.groupby(['User_id','Coupon_id']).agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c1,on=['User_id','Coupon_id'])

c2 = dataset3[['User_id','Coupon_id','Date_received']]
c2.Date_received = c2.Date_received.astype('str')
c2 = c2.groupby(['User_id','Coupon_id'])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()

# 领取特定优惠券数量
c2['received_number'] = c2.Date_received.apply(lambda x:len(x.split(':')))
# 领取特定优惠券最晚时间
c2['max_date_received'] = c2.Date_received.apply(lambda s:max([int(d) for d in s.split(":")]))
# 领取特定优惠券最早时间
c2['min_date_received'] = c2.Date_received.apply(lambda s: min( [int(d) for d in s.split(":")]))
c2 = c2[['User_id','Coupon_id','received_number','max_date_received','min_date_received']]
other_feature3 = pd.merge(other_feature3,c2,on=['User_id','Coupon_id'])


other_feature3['this_month_user_received_same_coupon_islastone'] = other_feature3.max_date_received - other_feature3.Date_received
other_feature3['this_month_user_received_same_coupon_isfirstone'] = other_feature3.Date_received - other_feature3.min_date_received

def is_firstlastone(x):
    "判断该用户是否为第一次/最后一次领取该卷"
    if x == 0:
        return 1
    else :
        return 0
other_feature3.this_month_user_received_same_coupon_isfirstone = other_feature3.this_month_user_received_same_coupon_isfirstone.apply(is_firstlastone)
other_feature3.this_month_user_received_same_coupon_islastone = other_feature3.this_month_user_received_same_coupon_islastone.apply(is_firstlastone)


c4 = dataset3[['User_id','Date_received']]
#  该用户当天领取优惠券数目
c4['this_day_user_received_coupon_count'] = 1
c4 = c4.groupby(['User_id','Date_received']).agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c4,on=['User_id','Date_received'])

c5 = dataset3[['User_id','Coupon_id','Date_received']]
# 该用户当天领取特定优惠券数目
c5['this_day_user_received_same_coupon_count'] = 1
c5 = c5.groupby(['User_id','Coupon_id','Date_received']).agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c5,on=['User_id','Coupon_id','Date_received'])

c6 = dataset3[['User_id','Coupon_id','Date_received']]
c6.Date_received = c6.Date_received.astype('str')
c6 = c6.groupby(['User_id','Coupon_id',])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
c6.rename(columns={'Date_received':'dates'},inplace=True)

def get_day_gap_before(s):

    date_received, dates = s.split('-')
    dates = dates.split(':')
    gaps = []
    for d in dates:
        this_gap =  (date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))-date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))).days
        if this_gap > 0:
            gaps.append(this_gap)
    if len(gaps) == 0:
        return -1
    else:
        return min(gaps)

def get_day_gap_after(s):
    date_received, dates = s.split('-')
    dates = dates.split(':')
    gaps = []
    for d in dates:
        this_gap = (date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))-date.date(int(date_received[0:4]), int(date_received[4:6]),int(date_received[6:8]))).days
        if this_gap > 0:
            gaps.append(this_gap)
    if len(gaps) == 0:
        return -1
    else:
        return min(gaps)

def get_user_day_before_all_coupon_count(s):
    "获取该用户当天之前领取的特定（所有）优惠券数目"
    date_received,dates = s.split('-')
    count = 0
    for d in dates.split(':'):
        this_gap = (date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))-date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))).days
        if this_gap > 0:
            count +=1
    return count

def get_user_day_after_all_coupon_count(s):
    "取该用户当天之后领取的特定（所有）优惠券数目"
    date_received, dates = s.split('-')
    count = 0
    for d in dates.split(':'):
        this_gap = (date.date(int(d[0:4]),int(d[4:6]),int(d[6:8])) -  date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))).days
        if this_gap > 0:
            count += 1
    return count

# 该用户该天领取特定优惠券距离最近一次领取前后的领取时间 间隔为0则为-1

other_feature3 = pd.merge(other_feature3 ,c6, on=['User_id','Coupon_id'],how = 'left')
other_feature3['date_received_date'] = other_feature3.Date_received.astype('str') + '-' + other_feature3.dates
other_feature3['same_coupon_day_gap_before'] = other_feature3.date_received_date.apply(get_day_gap_before)
other_feature3['same_coupon_day_gap_after'] = other_feature3.date_received_date.apply(get_day_gap_after)
# 用户此次之后/前领取的特定优惠券数目
other_feature3['same_coupon_day_count_after'] = other_feature3.date_received_date.apply(get_user_day_after_all_coupon_count)
other_feature3['same_coupon_day_count_before'] = other_feature3.date_received_date.apply(get_user_day_before_all_coupon_count)
other_feature3.drop(['dates','date_received_date'],axis =1,inplace = True)

c8 = dataset3[['User_id','Date_received']]
c8.Date_received = c8.Date_received.astype('str')
c8 = c8.groupby(['User_id'])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
c8.rename(columns={"Date_received":"dates"},inplace=True)

other_feature3 = pd.merge(other_feature3, c8, on=['User_id'],how='left')
other_feature3['date_received_dates'] = other_feature3.Date_received.astype('str') + '-' + other_feature3.dates
# 用户此次之后/前领取的所有优惠券数目
other_feature3['user_day_gap_before'] = other_feature3.date_received_dates.apply(get_user_day_before_all_coupon_count)
other_feature3['user_day_gap_after'] = other_feature3.date_received_dates.apply(get_user_day_after_all_coupon_count)
other_feature3.drop(['dates','date_received_dates'],axis=1,inplace=True)

# 该用户领取特定商家优惠券数目
c10 = dataset3[['User_id','Merchant_id']]
c10['user_same_merchant_coupon_counts'] = 1
c10 = c10.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c10,on=['User_id','Merchant_id'])

# 用户领取的不同商家数目
c11 = dataset3[['User_id','Merchant_id']]
c11.Merchant_id = c11.Merchant_id.astype('str')
c11 = c11.groupby(['User_id'])['Merchant_id'].agg(lambda x:':'.join(x)).reset_index()

def evaluate_diffmerchant(s):
    "计算不同商家数目"
    t = np.array(s.split(':'))
    t = np.unique(t)
    return len(t)
c11['diff_merchant_count'] = c11.Merchant_id.apply(evaluate_diffmerchant)
c11 = c11[['User_id','diff_merchant_count']]
other_feature3 = pd.merge(other_feature3,c11,on='User_id')


def get_user_all_diff_coupon_copunt(s):
    "获取用户领取优惠券种类"
    t = np.array(s.split('-'))
    t = np.unique(t)
    return len(t)

# 提取用户领取优惠券种类
c12 = dataset3[['User_id','Discount_rate']]
c12 = c12.groupby('User_id')['Discount_rate'].agg(lambda s:'-'.join(s)).reset_index()
c12['user_diff_coupon_count'] = c12.Discount_rate.apply(get_user_all_diff_coupon_copunt)
c12 = c12[['User_id','user_diff_coupon_count']]
other_feature3 = pd.merge(other_feature3,c12,on='User_id')


# 商家被领取优惠券数目
c13 = dataset3[['Merchant_id']]
c13['merchant_coupon_count'] = 1
c13 = c13.groupby('Merchant_id').agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c13,on='Merchant_id')
print(other_feature3.shape)

# 商家被领取特定优惠券数目
c14 = dataset3[['Merchant_id','Coupon_id']]
c14['merchant_same_coupon_count'] = 1
c14 = c14.groupby(['Merchant_id','Coupon_id']).agg('sum').reset_index()
other_feature3 = pd.merge(other_feature3,c14,on=['Merchant_id','Coupon_id'])

# 获取商家被多少不同用户领取的数目
c15 = dataset3[['Merchant_id','User_id']]
c15.User_id = c15.User_id.astype('str')
c15 = c15.groupby('Merchant_id')['User_id'].agg(lambda s:':'.join(s)).reset_index()
c15['merchant_all_diff_user_count'] = c15.User_id.apply(evaluate_diffmerchant)
c15 = c15[['Merchant_id','merchant_all_diff_user_count']]
other_feature3 = pd.merge(other_feature3,c15,on=['Merchant_id'])


# 获取商家发行的所有优惠券种类数目
c16 = dataset3[['Merchant_id','Discount_rate']]
c16 = c16.groupby('Merchant_id')['Discount_rate'].agg(lambda s:'-'.join(s)).reset_index()
c16['merchant_diff_coupon_count'] = c16.Discount_rate.apply(get_user_all_diff_coupon_copunt)
c16 = c16[['Merchant_id','merchant_diff_coupon_count']]
other_feature3 = pd.merge(other_feature3,c16,on=['Merchant_id'])
other_feature3.drop(['received_number', 'max_date_received', 'min_date_received'],axis = 1,inplace=True)
print(other_feature3.shape)
print(other_feature3.columns.values.tolist())
other_feature3.to_csv('characterEngineer/other_feature3.csv',index=None)

# for dataset2
other_feature2 = dataset2[['User_id','Merchant_id','Coupon_id','Date_received']]
print(other_feature2.shape)

c = dataset2[['User_id']]
# 该用户该月领取优惠券总数
c.loc[:,'this_month_user_reveive_count'] = 1
c = c.groupby('User_id').agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c,on='User_id')

c1 = dataset2[["User_id","Coupon_id"]]
# 该用户该月领取特定优惠券数目
c1.loc[:,'this_month_user_receive_same_coupon_count'] = 1
c1 = c1.groupby(['User_id','Coupon_id']).agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c1,on=['User_id','Coupon_id'])

c2 = dataset2[['User_id','Coupon_id','Date_received']]
c2.Date_received = c2.Date_received.astype('str')
c2 = c2.groupby(['User_id','Coupon_id'])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
print(c2.head())

# 领取特定优惠券数量
c2['received_number'] = c2.Date_received.apply(lambda x:len(x.split(':')))
# 领取特定优惠券最晚时间
c2['max_date_received'] = c2.Date_received.apply(lambda s:max([d for d in s.split(":")]))
# 领取特定优惠券最早时间
c2['min_date_received'] = c2.Date_received.apply(lambda s: min( [d for d in s.split(":")]))
c2 = c2[['User_id','Coupon_id','received_number','max_date_received','min_date_received']]
other_feature2 = pd.merge(other_feature2,c2,on=['User_id','Coupon_id'])


other_feature2['this_month_user_received_same_coupon_islastone'] = other_feature2.max_date_received.astype(np.float32) - other_feature2.Date_received.astype(np.float32)
other_feature2['this_month_user_received_same_coupon_isfirstone'] = other_feature2.Date_received.astype(np.float32) - other_feature2.min_date_received.astype(np.float32)

def is_firstlastone(x):
    "判断该用户是否为第一次/最后一次领取该卷"
    if x == 0:
        return 1
    else :
        return 0
other_feature2.this_month_user_received_same_coupon_isfirstone = other_feature2.this_month_user_received_same_coupon_isfirstone.apply(is_firstlastone)
other_feature2.this_month_user_received_same_coupon_islastone = other_feature2.this_month_user_received_same_coupon_islastone.apply(is_firstlastone)


c4 = dataset2[['User_id','Date_received']]
#  该用户当天领取优惠券数目
c4['this_day_user_received_coupon_count'] = 1
c4 = c4.groupby(['User_id','Date_received']).agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c4,on=['User_id','Date_received'])

c5 = dataset2[['User_id','Coupon_id','Date_received']]
# 该用户当天领取特定优惠券数目
c5['this_day_user_received_same_coupon_count'] = 1
c5 = c5.groupby(['User_id','Coupon_id','Date_received']).agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c5,on=['User_id','Coupon_id','Date_received'])

c6 = dataset2[['User_id','Coupon_id','Date_received']]
c6.Date_received = c6.Date_received.astype('str')
c6 = c6.groupby(['User_id','Coupon_id',])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
c6.rename(columns={'Date_received':'dates'},inplace=True)

def get_day_gap_before(s):

    date_received, dates = s.split('-')
    dates = dates.split(':')
    gaps = []
    for d in dates:
        this_gap =  (date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))-date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))).days
        if this_gap > 0:
            gaps.append(this_gap)
    if len(gaps) == 0:
        return -1
    else:
        return min(gaps)

def get_day_gap_after(s):
    date_received, dates = s.split('-')
    dates = dates.split(':')
    gaps = []
    for d in dates:
        this_gap = (date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))-date.date(int(date_received[0:4]), int(date_received[4:6]),int(date_received[6:8]))).days
        if this_gap > 0:
            gaps.append(this_gap)
    if len(gaps) == 0:
        return -1
    else:
        return min(gaps)

def get_user_day_before_all_coupon_count(s):
    "获取该用户当天之前领取的特定（所有）优惠券数目"
    date_received,dates = s.split('-')
    count = 0
    for d in dates.split(':'):
        this_gap = (date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))-date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))).days
        if this_gap > 0:
            count +=1
    return count

def get_user_day_after_all_coupon_count(s):
    "取该用户当天之后领取的特定（所有）优惠券数目"
    date_received, dates = s.split('-')
    count = 0
    for d in dates.split(':'):
        this_gap = (date.date(int(d[0:4]),int(d[4:6]),int(d[6:8])) -  date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))).days
        if this_gap > 0:
            count += 1
    return count

# 该用户该天领取特定优惠券距离最近一次领取前后的领取时间 间隔为0则为-1

other_feature2 = pd.merge(other_feature2 ,c6, on=['User_id','Coupon_id'],how = 'left')
other_feature2['date_received_date'] = other_feature2.Date_received.astype('str') + '-' + other_feature2.dates
other_feature2['same_coupon_day_gap_before'] = other_feature2.date_received_date.apply(get_day_gap_before)
other_feature2['same_coupon_day_gap_after'] = other_feature2.date_received_date.apply(get_day_gap_after)
# 用户此次之后/前领取的特定优惠券数目
other_feature2['same_coupon_day_count_after'] = other_feature2.date_received_date.apply(get_user_day_after_all_coupon_count)
other_feature2['same_coupon_day_count_before'] = other_feature2.date_received_date.apply(get_user_day_before_all_coupon_count)
other_feature2.drop(['dates','date_received_date'],axis =1,inplace = True)

c8 = dataset2[['User_id','Date_received']]
c8.Date_received = c8.Date_received.astype('str')
c8 = c8.groupby(['User_id'])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
c8.rename(columns={"Date_received":"dates"},inplace=True)

other_feature2 = pd.merge(other_feature2, c8, on=['User_id'],how='left')
other_feature2['date_received_dates'] = other_feature2.Date_received.astype('str') + '-' + other_feature2.dates
# 用户此次之后/前领取的所有优惠券数目
other_feature2['user_day_gap_before'] = other_feature2.date_received_dates.apply(get_user_day_before_all_coupon_count)
other_feature2['user_day_gap_after'] = other_feature2.date_received_dates.apply(get_user_day_after_all_coupon_count)
other_feature2.drop(['dates','date_received_dates'],axis=1,inplace=True)

# 该用户领取特定商家优惠券数目
c10 = dataset2[['User_id','Merchant_id']]
c10['user_same_merchant_coupon_counts'] = 1
c10 = c10.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c10,on=['User_id','Merchant_id'])

# 用户领取的不同商家数目
c11 = dataset2[['User_id','Merchant_id']]
c11.Merchant_id = c11.Merchant_id.astype('str')
c11 = c11.groupby(['User_id'])['Merchant_id'].agg(lambda x:':'.join(x)).reset_index()


def evaluate_diffmerchant(s):
    "计算不同商家数目"
    t = np.array(s.split(':'))
    t = np.unique(t)
    return len(t)
c11['diff_merchant_count'] = c11.Merchant_id.apply(evaluate_diffmerchant)
c11 = c11[['User_id','diff_merchant_count']]
other_feature2 = pd.merge(other_feature2,c11,on='User_id')


def get_user_all_diff_coupon_copunt(s):
    "获取用户领取优惠券种类"
    t = np.array(s.split('-'))
    t = np.unique(t)
    return len(t)

# 提取用户领取优惠券种类
c12 = dataset2[['User_id','Discount_rate']]
c12 = c12.groupby('User_id')['Discount_rate'].agg(lambda s:'-'.join(s)).reset_index()
c12['user_diff_coupon_count'] = c12.Discount_rate.apply(get_user_all_diff_coupon_copunt)
c12 = c12[['User_id','user_diff_coupon_count']]
other_feature2 = pd.merge(other_feature2,c12,on='User_id')

# 商家被领取优惠券数目
c13 = dataset2[['Merchant_id']]
c13['merchant_coupon_count'] = 1
c13 = c13.groupby('Merchant_id').agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c13,on='Merchant_id')

# 商家被领取特定优惠券数目
c14 = dataset2[['Merchant_id','Coupon_id']]
c14['merchant_same_coupon_count'] = 1
c14 = c14.groupby(['Merchant_id','Coupon_id']).agg('sum').reset_index()
other_feature2 = pd.merge(other_feature2,c14,on=['Merchant_id','Coupon_id'])

# 获取商家被多少不同用户领取的数目
c15 = dataset2[['Merchant_id','User_id']]
c15.User_id = c15.User_id.astype('str')
c15 = c15.groupby('Merchant_id')['User_id'].agg(lambda s:':'.join(s)).reset_index()
c15['merchant_all_diff_user_count'] = c15.User_id.apply(evaluate_diffmerchant)
c15 = c15[['Merchant_id','merchant_all_diff_user_count']]
other_feature2 = pd.merge(other_feature2,c15,on=['Merchant_id'])

# 获取商家发行的所有优惠券种类数目
c16 = dataset2[['Merchant_id','Discount_rate']]
c16 = c16.groupby('Merchant_id')['Discount_rate'].agg(lambda s:'-'.join(s)).reset_index()
c16['merchant_diff_coupon_count'] = c16.Discount_rate.apply(get_user_all_diff_coupon_copunt)
c16 = c16[['Merchant_id','merchant_diff_coupon_count']]
other_feature2 = pd.merge(other_feature2,c16,on=['Merchant_id'])
other_feature2.drop(['received_number', 'max_date_received', 'min_date_received'],axis = 1,inplace=True)
print(other_feature2.shape)
print(other_feature2.columns.values.tolist())
other_feature2.to_csv('characterEngineer/other_feature2.csv',index=None)

# for dataset1
other_feature1 = dataset1[['User_id','Merchant_id','Coupon_id','Date_received']]
print(other_feature1.shape)

c = dataset1[['User_id']]
# 该用户该月领取优惠券总数
c.loc[:,'this_month_user_reveive_count'] = 1
c = c.groupby('User_id').agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c,on='User_id')

c1 = dataset1[["User_id","Coupon_id"]]
# 该用户该月领取特定优惠券数目
c1.loc[:,'this_month_user_receive_same_coupon_count'] = 1
c1 = c1.groupby(['User_id','Coupon_id']).agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c1,on=['User_id','Coupon_id'])

c2 = dataset1[['User_id','Coupon_id','Date_received']]
c2.Date_received = c2.Date_received.astype('str')
c2 = c2.groupby(['User_id','Coupon_id'])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()

# 领取特定优惠券数量
c2['received_number'] = c2.Date_received.apply(lambda x:len(x.split(':')))
# 领取特定优惠券最晚时间
c2['max_date_received'] = c2.Date_received.apply(lambda s:max([d for d in s.split(":")]))
# 领取特定优惠券最早时间
c2['min_date_received'] = c2.Date_received.apply(lambda s: min( [d for d in s.split(":")]))
c2 = c2[['User_id','Coupon_id','received_number','max_date_received','min_date_received']]
other_feature1 = pd.merge(other_feature1,c2,on=['User_id','Coupon_id'])


other_feature1['this_month_user_received_same_coupon_islastone'] = other_feature1.max_date_received.astype(np.float32) - other_feature1.Date_received.astype(np.float32)
other_feature1['this_month_user_received_same_coupon_isfirstone'] = other_feature1.Date_received.astype(np.float32)  - other_feature1.min_date_received.astype(np.float32)

def is_firstlastone(x):
    "判断该用户是否为第一次/最后一次领取该卷"
    if x == 0:
        return 1
    else :
        return 0
other_feature1.this_month_user_received_same_coupon_isfirstone = other_feature1.this_month_user_received_same_coupon_isfirstone.apply(is_firstlastone)
other_feature1.this_month_user_received_same_coupon_islastone = other_feature1.this_month_user_received_same_coupon_islastone.apply(is_firstlastone)


c4 = dataset1[['User_id','Date_received']]
#  该用户当天领取优惠券数目
c4['this_day_user_received_coupon_count'] = 1
c4 = c4.groupby(['User_id','Date_received']).agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c4,on=['User_id','Date_received'])

c5 = dataset1[['User_id','Coupon_id','Date_received']]
# 该用户当天领取特定优惠券数目
c5['this_day_user_received_same_coupon_count'] = 1
c5 = c5.groupby(['User_id','Coupon_id','Date_received']).agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c5,on=['User_id','Coupon_id','Date_received'])

c6 = dataset1[['User_id','Coupon_id','Date_received']]
c6.Date_received = c6.Date_received.astype('str')
c6 = c6.groupby(['User_id','Coupon_id',])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
c6.rename(columns={'Date_received':'dates'},inplace=True)

def get_day_gap_before(s):

    date_received, dates = s.split('-')
    dates = dates.split(':')
    gaps = []
    for d in dates:
        this_gap =  (date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))-date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))).days
        if this_gap > 0:
            gaps.append(this_gap)
    if len(gaps) == 0:
        return -1
    else:
        return min(gaps)

def get_day_gap_after(s):
    date_received, dates = s.split('-')
    dates = dates.split(':')
    gaps = []
    for d in dates:
        this_gap = (date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))-date.date(int(date_received[0:4]), int(date_received[4:6]),int(date_received[6:8]))).days
        if this_gap > 0:
            gaps.append(this_gap)
    if len(gaps) == 0:
        return -1
    else:
        return min(gaps)

def get_user_day_before_all_coupon_count(s):
    "获取该用户当天之前领取的特定（所有）优惠券数目"
    date_received,dates = s.split('-')
    count = 0
    for d in dates.split(':'):
        this_gap = (date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))-date.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))).days
        if this_gap > 0:
            count +=1
    return count

def get_user_day_after_all_coupon_count(s):
    "取该用户当天之后领取的特定（所有）优惠券数目"
    date_received, dates = s.split('-')
    count = 0
    for d in dates.split(':'):
        this_gap = (date.date(int(d[0:4]),int(d[4:6]),int(d[6:8])) -  date.date(int(date_received[0:4]),int(date_received[4:6]),int(date_received[6:8]))).days
        if this_gap > 0:
            count += 1
    return count

# 该用户该天领取特定优惠券距离最近一次领取前后的领取时间 间隔为0则为-1

other_feature1 = pd.merge(other_feature1 ,c6, on=['User_id','Coupon_id'],how = 'left')
other_feature1['date_received_date'] = other_feature1.Date_received.astype('str') + '-' + other_feature1.dates
other_feature1['same_coupon_day_gap_before'] = other_feature1.date_received_date.apply(get_day_gap_before)
other_feature1['same_coupon_day_gap_after'] = other_feature1.date_received_date.apply(get_day_gap_after)
# 用户此次之后/前领取的特定优惠券数目
other_feature1['same_coupon_day_count_after'] = other_feature1.date_received_date.apply(get_user_day_after_all_coupon_count)
other_feature1['same_coupon_day_count_before'] = other_feature1.date_received_date.apply(get_user_day_before_all_coupon_count)
other_feature1.drop(['dates','date_received_date'],axis =1,inplace = True)

c8 = dataset1[['User_id','Date_received']]
c8.Date_received = c8.Date_received.astype('str')
c8 = c8.groupby(['User_id'])['Date_received'].agg(lambda x: ':'.join(x)).reset_index()
c8.rename(columns={"Date_received":"dates"},inplace=True)

other_feature1 = pd.merge(other_feature1, c8, on=['User_id'],how='left')
other_feature1['date_received_dates'] = other_feature1.Date_received.astype('str') + '-' + other_feature1.dates
# 用户此次之后/前领取的所有优惠券数目
other_feature1['user_day_gap_before'] = other_feature1.date_received_dates.apply(get_user_day_before_all_coupon_count)
other_feature1['user_day_gap_after'] = other_feature1.date_received_dates.apply(get_user_day_after_all_coupon_count)
other_feature1.drop(['dates','date_received_dates'],axis=1,inplace=True)

# 该用户领取特定商家优惠券数目
c10 = dataset1[['User_id','Merchant_id']]
c10['user_same_merchant_coupon_counts'] = 1
c10 = c10.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c10,on=['User_id','Merchant_id'])

# 用户领取的不同商家数目
c11 = dataset1[['User_id','Merchant_id']]
c11.Merchant_id = c11.Merchant_id.astype('str')
c11 = c11.groupby(['User_id'])['Merchant_id'].agg(lambda x:':'.join(x)).reset_index()

def evaluate_diffmerchant(s):
    "计算不同商家数目"
    t = np.array(s.split(':'))
    t = np.unique(t)
    return len(t)
c11['diff_merchant_count'] = c11.Merchant_id.apply(evaluate_diffmerchant)
c11 = c11[['User_id','diff_merchant_count']]
other_feature1 = pd.merge(other_feature1,c11,on='User_id')

def get_user_all_diff_coupon_copunt(s):
    "获取用户领取优惠券种类"
    t = np.array(s.split('-'))
    t = np.unique(t)
    return len(t)

# 提取用户领取优惠券种类
c12 = dataset1[['User_id','Discount_rate']]
c12 = c12.groupby('User_id')['Discount_rate'].agg(lambda s:'-'.join(s)).reset_index()
c12['user_diff_coupon_count'] = c12.Discount_rate.apply(get_user_all_diff_coupon_copunt)
c12 = c12[['User_id','user_diff_coupon_count']]
other_feature1 = pd.merge(other_feature1,c12,on='User_id')

# 商家被领取优惠券数目
c13 = dataset1[['Merchant_id']]
c13['merchant_coupon_count'] = 1
c13 = c13.groupby('Merchant_id').agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c13,on='Merchant_id')

# 商家被领取特定优惠券数目
c14 = dataset1[['Merchant_id','Coupon_id']]
c14['merchant_same_coupon_count'] = 1
c14 = c14.groupby(['Merchant_id','Coupon_id']).agg('sum').reset_index()
other_feature1 = pd.merge(other_feature1,c14,on=['Merchant_id','Coupon_id'])

# 获取商家被多少不同用户领取的数目
c15 = dataset1[['Merchant_id','User_id']]
c15.User_id = c15.User_id.astype('str')
c15 = c15.groupby('Merchant_id')['User_id'].agg(lambda s:':'.join(s)).reset_index()
c15['merchant_all_diff_user_count'] = c15.User_id.apply(evaluate_diffmerchant)
c15 = c15[['Merchant_id','merchant_all_diff_user_count']]
other_feature1 = pd.merge(other_feature1,c15,on=['Merchant_id'])

# 获取商家发行的所有优惠券种类数目
c16 = dataset1[['Merchant_id','Discount_rate']]
c16 = c16.groupby('Merchant_id')['Discount_rate'].agg(lambda s:'-'.join(s)).reset_index()
c16['merchant_diff_coupon_count'] = c16.Discount_rate.apply(get_user_all_diff_coupon_copunt)
c16 = c16[['Merchant_id','merchant_diff_coupon_count']]
other_feature1 = pd.merge(other_feature1,c16,on=['Merchant_id'])
other_feature1.drop(['received_number', 'max_date_received', 'min_date_received'],axis = 1,inplace=True)
print(other_feature1.shape)
print(other_feature1.columns.values.tolist())
other_feature1.to_csv('characterEngineer/other_feature1.csv',index=None)