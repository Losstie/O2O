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
feature3 = off_train[((off_train.Date>='20160315')&(off_train.Date<='20160630'))|((off_train.Date=='null')&(off_train.Date_received>='20160315')&(off_train.Date_received<='20160630'))]
dataset2 = off_train[(off_train.Date_received>='20160515')&(off_train.Date_received<='20160615')]
feature2 = off_train[(off_train.Date>='20160201')&(off_train.Date<='20160514')|((off_train.Date=='null')&(off_train.Date_received>='20160201')&(off_train.Date_received<='20160514'))]
dataset1 = off_train[(off_train.Date_received>='20160414')&(off_train.Date_received<='20160514')]
feature1 = off_train[(off_train.Date>='20160101')&(off_train.Date<='20160413')|((off_train.Date=='null')&(off_train.Date_received>='20160101')&(off_train.Date_received<='20160413'))]

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

# 领取特定优惠券数量
c2['received_number'] = c2.Date_received.apply(lambda x:len(x.split(':')))
# 领取特定优惠券最晚时间
c2['max_date_received'] = c2.Date_received.apply(lambda s:max([int(d) for d in s.split(":")]))
# 领取特定优惠券最早时间
c2['min_date_received'] = c2.Date_received.apply(lambda s: min( [int(d) for d in s.split(":")]))
c2 = c2[['User_id','Coupon_id','received_number','max_date_received','min_date_received']]
other_feature2 = pd.merge(other_feature2,c2,on=['User_id','Coupon_id'])


other_feature2['this_month_user_received_same_coupon_islastone'] = other_feature2.max_date_received - other_feature2.Date_received.astype('int')
other_feature2['this_month_user_received_same_coupon_isfirstone'] = other_feature2.Date_received.astype('int') - other_feature2.min_date_received

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
c2['max_date_received'] = c2.Date_received.apply(lambda s:max([int(d) for d in s.split(":")]))
# 领取特定优惠券最早时间
c2['min_date_received'] = c2.Date_received.apply(lambda s: min( [int(d) for d in s.split(":")]))
c2 = c2[['User_id','Coupon_id','received_number','max_date_received','min_date_received']]
other_feature1 = pd.merge(other_feature1,c2,on=['User_id','Coupon_id'])


other_feature1['this_month_user_received_same_coupon_islastone'] = other_feature1.max_date_received - other_feature1.Date_received.astype('int')
other_feature1['this_month_user_received_same_coupon_isfirstone'] = other_feature1.Date_received.astype('int') - other_feature1.min_date_received

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
dataset1 = pd.merge(dataset1,d,on='Coupon_id',how='left')
dataset1.to_csv('characterEngineer/coupon1_feature.csv',index=None)

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

c1 = merchant3[merchant3.Date!='null'][['Merchant_id']]
c1['total_sales'] = 1
c1 = c1.groupby('Merchant_id').agg('sum').reset_index()

c2 = merchant3[(merchant3.Date!='null')&(merchant3.Coupon_id!='null')][['Merchant_id']]
c2['sales_use_coupon'] = 1
c2 = c2.groupby('Merchant_id').agg('sum').reset_index()

c3 = merchant3[merchant3.Coupon_id!='null'][['Merchant_id']]
c3['total_coupon'] = 1
c3 = c3.groupby('Merchant_id').agg('sum').reset_index()

c4 = merchant3[(merchant3.Date!='null')&(merchant3.Coupon_id!='null')][['Merchant_id','Distance']]
c4.replace('null',-1,inplace=True)
c4.Distance = c4.Distance.astype('int')
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
merchant3_feature['merchant_coupon_transfer_rate'] = merchant3_feature.sales_use_coupon.astype('float') / merchant3_feature.total_coupon
merchant3_feature['coupon_rate'] = merchant3_feature.sales_use_coupon.astype('float') / merchant3_feature.total_sales
merchant3_feature.total_coupon = merchant3_feature.total_coupon.replace(np.nan,0) #fillna with 0
merchant3_feature.to_csv('characterEngineer/merchant3_feature.csv',index=None)
print(merchant3_feature.shape)

# for feature2
merchant2 = feature2[['Merchant_id','Coupon_id','Distance','Date_received','Date']]
c = merchant2[['Merchant_id']]
c.drop_duplicates(inplace=True)

c1 = merchant2[merchant2.Date!='null'][['Merchant_id']]
c1['total_sales'] = 1
c1 = c1.groupby('Merchant_id').agg('sum').reset_index()

c2 = merchant2[(merchant2.Date!='null')&(merchant2.Coupon_id!='null')][['Merchant_id']]
c2['sales_use_coupon'] = 1
c2 = c2.groupby('Merchant_id').agg('sum').reset_index()

c3 = merchant2[merchant2.Coupon_id!='null'][['Merchant_id']]
c3['total_coupon'] = 1
c3 = c3.groupby('Merchant_id').agg('sum').reset_index()

c4 = merchant2[(merchant2.Date!='null')&(merchant2.Coupon_id!='null')][['Merchant_id','Distance']]
c4.replace('null',-1,inplace=True)
c4.Distance = c4.Distance.astype('int')
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
merchant2_feature['merchant_coupon_transfer_rate'] = merchant2_feature.sales_use_coupon.astype('float') / merchant2_feature.total_coupon
merchant2_feature['coupon_rate'] = merchant2_feature.sales_use_coupon.astype('float') / merchant2_feature.total_sales
merchant2_feature.total_coupon = merchant2_feature.total_coupon.replace(np.nan,0) #fillna with 0
merchant2_feature.to_csv('characterEngineer/merchant2_feature.csv',index=None)
print(merchant2_feature.shape)

# for feature1
merchant1 = feature1[['Merchant_id','Coupon_id','Distance','Date_received','Date']]
c = merchant1[['Merchant_id']]
c.drop_duplicates(inplace=True)

c1 = merchant1[merchant1.Date!='null'][['Merchant_id']]
c1['total_sales'] = 1
c1 = c1.groupby('Merchant_id').agg('sum').reset_index()

c2 = merchant1[(merchant1.Date!='null')&(merchant1.Coupon_id!='null')][['Merchant_id']]
c2['sales_use_coupon'] = 1
c2 = c2.groupby('Merchant_id').agg('sum').reset_index()

c3 = merchant1[merchant1.Coupon_id!='null'][['Merchant_id']]
c3['total_coupon'] = 1
c3 = c3.groupby('Merchant_id').agg('sum').reset_index()

c4 = merchant1[(merchant1.Date!='null')&(merchant1.Coupon_id!='null')][['Merchant_id','Distance']]
c4.replace('null',-1,inplace=True)
c4.Distance = c4.Distance.astype('int')
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
merchant1_feature['merchant_coupon_transfer_rate'] = merchant1_feature.sales_use_coupon.astype('float') / merchant1_feature.total_coupon
merchant1_feature['coupon_rate'] = merchant1_feature.sales_use_coupon.astype('float') / merchant1_feature.total_sales
merchant1_feature.total_coupon = merchant1_feature.total_coupon.replace(np.nan,0) #fillna with 0
merchant1_feature.to_csv('characterEngineer/merchant1_feature.csv',index=None)
print(merchant1_feature.shape)

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

c1 = user3[user3.Date!='null'][['User_id','Merchant_id']]
c1.drop_duplicates(inplace=True)
c1.Merchant_id = 1
c1 = c1.groupby('User_id').agg('sum').reset_index()
c1.rename(columns={'Merchant_id':'count_merchant'},inplace=True)

c2 = user3[(user3.Date!='null')&(user3.Coupon_id!='null')][['User_id','Distance']]
c2.replace('null',-1,inplace=True)
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

c7 = user3[(user3.Date!='null')&(user3.Coupon_id!='null')][['User_id']]
c7['buy_use_coupon'] = 1
c7 = c7.groupby('User_id').agg('sum').reset_index()

c8 = user3[user3.Date!='null'][['User_id']]
c8['buy_total'] = 1
c8 = c8.groupby('User_id').agg('sum').reset_index()

c9 = user3[user3.Coupon_id!='null'][['User_id']]
c9['coupon_received'] = 1
c9 = c9.groupby('User_id').agg('sum').reset_index()

c10 = user3[(user3.Date_received!='null')&(user3.Date!='null')][['User_id','Date_received','Date']]
c10['user_date_datereceived_gap'] = c10.Date + ':' + c10.Date_received
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

c1 = user2[user2.Date!='null'][['User_id','Merchant_id']]
c1.drop_duplicates(inplace=True)
c1.Merchant_id = 1
c1 = c1.groupby('User_id').agg('sum').reset_index()
c1.rename(columns={'Merchant_id':'count_merchant'},inplace=True)

c2 = user2[(user2.Date!='null')&(user2.Coupon_id!='null')][['User_id','Distance']]
c2.replace('null',-1,inplace=True)
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

c7 = user2[(user2.Date!='null')&(user2.Coupon_id!='null')][['User_id']]
c7['buy_use_coupon'] = 1
c7 = c7.groupby('User_id').agg('sum').reset_index()

c8 = user2[user2.Date!='null'][['User_id']]
c8['buy_total'] = 1
c8 = c8.groupby('User_id').agg('sum').reset_index()

c9 = user2[user2.Coupon_id!='null'][['User_id']]
c9['coupon_received'] = 1
c9 = c9.groupby('User_id').agg('sum').reset_index()

c10 = user2[(user2.Date_received!='null')&(user2.Date!='null')][['User_id','Date_received','Date']]
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

c1 = user1[user1.Date!='null'][['User_id','Merchant_id']]
c1.drop_duplicates(inplace=True)
c1.Merchant_id = 1
c1 = c1.groupby('User_id').agg('sum').reset_index()
c1.rename(columns={'Merchant_id':'count_merchant'},inplace=True)

c2 = user1[(user1.Date!='null')&(user1.Coupon_id!='null')][['User_id','Distance']]
c2.replace('null',-1,inplace=True)
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

c7 = user1[(user1.Date!='null')&(user1.Coupon_id!='null')][['User_id']]
c7['buy_use_coupon'] = 1
c7 = c7.groupby('User_id').agg('sum').reset_index()

c8 = user1[user1.Date!='null'][['User_id']]
c8['buy_total'] = 1
c8 = c8.groupby('User_id').agg('sum').reset_index()

c9 = user1[user1.Coupon_id!='null'][['User_id']]
c9['coupon_received'] = 1
c9 = c9.groupby('User_id').agg('sum').reset_index()

c10 = user1[(user1.Date_received!='null')&(user1.Date!='null')][['User_id','Date_received','Date']]
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
user1_feature.to_csv('characterEngineer/user1_feature.csv',index=None)

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
c = feature3[['User_id','Merchant_id','Coupon_id','Date_received','Date']]

c1 = c[['User_id','Merchant_id','Coupon_id']]
c1 = c1[c1.Coupon_id != 'null' ]
c1['user_merchant_received_coupon_count'] = 1
c1 = c1.groupby(['User_id','Merchant_id']).agg('sum').reset_index()

c2 = c[['User_id','Merchant_id','Date']]
c2 = c2[c2.Date != 'null']
c2['user_merchant_sales_count'] = 1
c2 = c2.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
user_merchant3_feature = pd.merge(c1, c2,on=['User_id','Merchant_id'])

c3 = c[['User_id','Merchant_id','Coupon_id','Date']]
c3 = c3[(c3.Coupon_id != 'null')&(c3.Date != 'null')]
c3 = c3[['User_id','Merchant_id']]
c3['user_merchant_usecoupon_sales_count'] = 1
c3 = c3.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
user_merchant3_feature = pd.merge(user_merchant3_feature, c3,on=['User_id','Merchant_id'],how='left')
user_merchant3_feature.user_merchant_sales_count = user_merchant3_feature.user_merchant_sales_count.replace(np.nan, 0)
user_merchant3_feature.user_merchant_usecoupon_sales_count = user_merchant3_feature.user_merchant_usecoupon_sales_count.replace(np.nan, 0)
user_merchant3_feature['user_merchant_receivedcoupon_notuse_count'] = user_merchant3_feature.user_merchant_received_coupon_count - user_merchant3_feature.user_merchant_usecoupon_sales_count
user_merchant3_feature['user_merchant_usecoupon_sales_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.user_merchant_received_coupon_count
user_merchant3_feature['user_merchant_coupon_transfer_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.user_merchant_sales_count
user_merchant3_feature.user_merchant_coupon_transfer_rate = user_merchant3_feature.user_merchant_coupon_transfer_rate.replace(np.nan, 0)

c4 = c[['User_id','Coupon_id']]
c4 = c4[c4.Coupon_id != 'null']
c4['user_received_coupon_count'] = 1
c4 = c4.groupby('User_id').agg('sum').reset_index()

c5 = c[['User_id','Coupon_id','Date']]
c5 = c5[(c5.Coupon_id !='null')&(c5.Date !='null')]
c5 = c5[['User_id']]
c5['user_received_coupon_use_count'] =1
c5 = c5.groupby(['User_id']).agg('sum').reset_index()
c5 = pd.merge(c4, c5,on=['User_id']).reset_index()
c5.user_received_coupon_use_count = c5.user_received_coupon_use_count.replace(np.nan, 0)
c5['user_received_coupon_notuse_count'] = c5.user_received_coupon_count - c5.user_received_coupon_use_count
c5 = c5[['User_id','user_received_coupon_use_count','user_received_coupon_notuse_count']]

c6 = c[['Merchant_id','Coupon_id']]
c6 = c6[c6.Coupon_id != 'null']
c6 = c6[['Merchant_id']]
c6['merchant_coupon_sum'] = 1
c6 = c6.groupby(['Merchant_id']).agg('sum').reset_index()

c7 = c[['Merchant_id','Coupon_id','Date']]
c7 = c7[(c7.Coupon_id != 'null')&(c7.Date !='null')]
c7 = c7[['Merchant_id']]
c7['merchant_coupon_used_count'] = 1
c7 = c7.groupby(['Merchant_id']).agg('sum').reset_index()
c7 = pd.merge(c6,c7,on=['Merchant_id']).reset_index()
c7.merchant_coupon_used_count = c7.merchant_coupon_used_count.replace(np.nan, 0)
c7['merchant_coupon_notuse_count'] = c7.merchant_coupon_sum - c7.merchant_coupon_used_count
c7 = c7[['Merchant_id','merchant_coupon_used_count','merchant_coupon_notuse_count']]

user_merchant3_feature = pd.merge(user_merchant3_feature, c7,on=['Merchant_id'],how='left')
user_merchant3_feature.merchant_coupon_used_count = user_merchant3_feature.merchant_coupon_used_count.replace(np.nan, 0)
user_merchant3_feature.merchant_coupon_notuse_count = user_merchant3_feature.merchant_coupon_notuse_count.replace(np.nan, 0)
user_merchant3_feature = pd.merge(user_merchant3_feature, c5,on=['User_id'],how='left')
user_merchant3_feature.user_received_coupon_use_count = user_merchant3_feature.user_received_coupon_use_count.replace(np.nan, 0)
user_merchant3_feature.user_received_coupon_notuse_count = user_merchant3_feature.user_received_coupon_notuse_count.replace(np.nan, 0)
user_merchant3_feature['user_merchant_foruser_received_coupon_notuse_rate'] = 1.0 * user_merchant3_feature.user_merchant_receivedcoupon_notuse_count / user_merchant3_feature.user_received_coupon_notuse_count
user_merchant3_feature['user_merchant_foruser_received_coupon_use_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.user_received_coupon_use_count
user_merchant3_feature['user_merchant_formerchant_received_coupon_notuse_rate'] = 1.0 * user_merchant3_feature.user_merchant_receivedcoupon_notuse_count / user_merchant3_feature.merchant_coupon_notuse_count
user_merchant3_feature['user_merchant_formerchant_received_coupon_use_rate'] = 1.0 * user_merchant3_feature.user_merchant_usecoupon_sales_count / user_merchant3_feature.merchant_coupon_used_count
user_merchant3_feature = user_merchant3_feature[['User_id','Merchant_id','user_merchant_received_coupon_count','user_merchant_sales_count',
                                                 'user_merchant_usecoupon_sales_count','user_merchant_receivedcoupon_notuse_count',
                                                 'user_merchant_usecoupon_sales_rate','user_merchant_coupon_transfer_rate',
                                                 'user_merchant_foruser_received_coupon_notuse_rate','user_merchant_foruser_received_coupon_use_rate',
                                                 'user_merchant_formerchant_received_coupon_notuse_rate','user_merchant_formerchant_received_coupon_use_rate']]
user_merchant3_feature.to_csv('characterEngineer/user_merchant3_feature.csv',index=None)
print(user_merchant3_feature.shape)

# for feature2
c = feature2[['User_id','Merchant_id','Coupon_id','Date_received','Date']]

c1 = c[['User_id','Merchant_id','Coupon_id']]
c1 = c1[c1.Coupon_id != 'null' ]
c1['user_merchant_received_coupon_count'] = 1
c1 = c1.groupby(['User_id','Merchant_id']).agg('sum').reset_index()

c2 = c[['User_id','Merchant_id','Date']]
c2 = c2[c2.Date != 'null']
c2['user_merchant_sales_count'] = 1
c2 = c2.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
user_merchant2_feature = pd.merge(c1, c2,on=['User_id','Merchant_id'])

c3 = c[['User_id','Merchant_id','Coupon_id','Date']]
c3 = c3[(c3.Coupon_id != 'null')&(c3.Date != 'null')]
c3 = c3[['User_id','Merchant_id']]
c3['user_merchant_usecoupon_sales_count'] = 1
c3 = c3.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
user_merchant2_feature = pd.merge(user_merchant2_feature, c3,on=['User_id','Merchant_id'],how='left')
user_merchant2_feature.user_merchant_sales_count = user_merchant2_feature.user_merchant_sales_count.replace(np.nan, 0)
user_merchant2_feature.user_merchant_usecoupon_sales_count = user_merchant2_feature.user_merchant_usecoupon_sales_count.replace(np.nan, 0)
user_merchant2_feature['user_merchant_receivedcoupon_notuse_count'] = user_merchant2_feature.user_merchant_received_coupon_count - user_merchant2_feature.user_merchant_usecoupon_sales_count
user_merchant2_feature['user_merchant_usecoupon_sales_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.user_merchant_received_coupon_count
user_merchant2_feature['user_merchant_coupon_transfer_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.user_merchant_sales_count
user_merchant2_feature.user_merchant_coupon_transfer_rate = user_merchant2_feature.user_merchant_coupon_transfer_rate.replace(np.nan, 0)

c4 = c[['User_id','Coupon_id']]
c4 = c4[c4.Coupon_id != 'null']
c4['user_received_coupon_count'] = 1
c4 = c4.groupby('User_id').agg('sum').reset_index()

c5 = c[['User_id','Coupon_id','Date']]
c5 = c5[(c5.Coupon_id !='null')&(c5.Date !='null')]
c5 = c5[['User_id']]
c5['user_received_coupon_use_count'] =1
c5 = c5.groupby(['User_id']).agg('sum').reset_index()
c5 = pd.merge(c4, c5,on=['User_id']).reset_index()
c5.user_received_coupon_use_count = c5.user_received_coupon_use_count.replace(np.nan, 0)
c5['user_received_coupon_notuse_count'] = c5.user_received_coupon_count - c5.user_received_coupon_use_count
c5 = c5[['User_id','user_received_coupon_use_count','user_received_coupon_notuse_count']]

c6 = c[['Merchant_id','Coupon_id']]
c6 = c6[c6.Coupon_id != 'null']
c6 = c6[['Merchant_id']]
c6['merchant_coupon_sum'] = 1
c6 = c6.groupby(['Merchant_id']).agg('sum').reset_index()

c7 = c[['Merchant_id','Coupon_id','Date']]
c7 = c7[(c7.Coupon_id != 'null')&(c7.Date !='null')]
c7 = c7[['Merchant_id']]
c7['merchant_coupon_used_count'] = 1
c7 = c7.groupby(['Merchant_id']).agg('sum').reset_index()
c7 = pd.merge(c6,c7,on=['Merchant_id']).reset_index()
c7.merchant_coupon_used_count = c7.merchant_coupon_used_count.replace(np.nan, 0)
c7['merchant_coupon_notuse_count'] = c7.merchant_coupon_sum - c7.merchant_coupon_used_count
c7 = c7[['Merchant_id','merchant_coupon_used_count','merchant_coupon_notuse_count']]

user_merchant2_feature = pd.merge(user_merchant2_feature, c7,on=['Merchant_id'],how='left')
user_merchant2_feature.merchant_coupon_used_count = user_merchant2_feature.merchant_coupon_used_count.replace(np.nan, 0)
user_merchant2_feature.merchant_coupon_notuse_count = user_merchant2_feature.merchant_coupon_notuse_count.replace(np.nan, 0)
user_merchant2_feature = pd.merge(user_merchant2_feature, c5,on=['User_id'],how='left')
user_merchant2_feature.user_received_coupon_use_count = user_merchant2_feature.user_received_coupon_use_count.replace(np.nan, 0)
user_merchant2_feature.user_received_coupon_notuse_count = user_merchant2_feature.user_received_coupon_notuse_count.replace(np.nan, 0)
user_merchant2_feature['user_merchant_foruser_received_coupon_notuse_rate'] = 1.0 * user_merchant2_feature.user_merchant_receivedcoupon_notuse_count / user_merchant2_feature.user_received_coupon_notuse_count
user_merchant2_feature['user_merchant_foruser_received_coupon_use_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.user_received_coupon_use_count
user_merchant2_feature['user_merchant_formerchant_received_coupon_notuse_rate'] = 1.0 * user_merchant2_feature.user_merchant_receivedcoupon_notuse_count / user_merchant2_feature.merchant_coupon_notuse_count
user_merchant2_feature['user_merchant_formerchant_received_coupon_use_rate'] = 1.0 * user_merchant2_feature.user_merchant_usecoupon_sales_count / user_merchant2_feature.merchant_coupon_used_count
user_merchant2_feature = user_merchant2_feature[['User_id','Merchant_id','user_merchant_received_coupon_count','user_merchant_sales_count',
                                                 'user_merchant_usecoupon_sales_count','user_merchant_receivedcoupon_notuse_count',
                                                 'user_merchant_usecoupon_sales_rate','user_merchant_coupon_transfer_rate',
                                                 'user_merchant_foruser_received_coupon_notuse_rate','user_merchant_foruser_received_coupon_use_rate',
                                                 'user_merchant_formerchant_received_coupon_notuse_rate','user_merchant_formerchant_received_coupon_use_rate']]
user_merchant2_feature.to_csv('characterEngineer/user_merchant2_feature.csv',index=None)
print(user_merchant2_feature.shape)

# for feature1
c = feature1[['User_id','Merchant_id','Coupon_id','Date_received','Date']]

c1 = c[['User_id','Merchant_id','Coupon_id']]
c1 = c1[c1.Coupon_id != 'null' ]
c1['user_merchant_received_coupon_count'] = 1
c1 = c1.groupby(['User_id','Merchant_id']).agg('sum').reset_index()


c2 = c[['User_id','Merchant_id','Date']]
c2 = c2[c2.Date != 'null']
c2['user_merchant_sales_count'] = 1
c2 = c2.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
user_merchant1_feature = pd.merge(c1, c2,on=['User_id','Merchant_id'])

c3 = c[['User_id','Merchant_id','Coupon_id','Date']]
c3 = c3[(c3.Coupon_id != 'null')&(c3.Date != 'null')]
c3 = c3[['User_id','Merchant_id']]
c3['user_merchant_usecoupon_sales_count'] = 1
c3 = c3.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
user_merchant1_feature = pd.merge(user_merchant1_feature, c3,on=['User_id','Merchant_id'],how='left')
user_merchant1_feature.user_merchant_sales_count = user_merchant1_feature.user_merchant_sales_count.replace(np.nan, 0)
user_merchant1_feature.user_merchant_usecoupon_sales_count = user_merchant1_feature.user_merchant_usecoupon_sales_count.replace(np.nan, 0)
user_merchant1_feature['user_merchant_receivedcoupon_notuse_count'] = user_merchant1_feature.user_merchant_received_coupon_count - user_merchant1_feature.user_merchant_usecoupon_sales_count
user_merchant1_feature['user_merchant_usecoupon_sales_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.user_merchant_received_coupon_count
user_merchant1_feature['user_merchant_coupon_transfer_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.user_merchant_sales_count
user_merchant1_feature.user_merchant_coupon_transfer_rate = user_merchant1_feature.user_merchant_coupon_transfer_rate.replace(np.nan, 0)

c4 = c[['User_id','Coupon_id']]
c4 = c4[c4.Coupon_id != 'null']
c4['user_received_coupon_count'] = 1
c4 = c4.groupby('User_id').agg('sum').reset_index()

c5 = c[['User_id','Coupon_id','Date']]
c5 = c5[(c5.Coupon_id !='null')&(c5.Date !='null')]
c5 = c5[['User_id']]
c5['user_received_coupon_use_count'] =1
c5 = c5.groupby(['User_id']).agg('sum').reset_index()
c5 = pd.merge(c4, c5,on=['User_id']).reset_index()
c5.user_received_coupon_use_count = c5.user_received_coupon_use_count.replace(np.nan, 0)
c5['user_received_coupon_notuse_count'] = c5.user_received_coupon_count - c5.user_received_coupon_use_count
c5 = c5[['User_id','user_received_coupon_use_count','user_received_coupon_notuse_count']]

c6 = c[['Merchant_id','Coupon_id']]
c6 = c6[c6.Coupon_id != 'null']
c6 = c6[['Merchant_id']]
c6['merchant_coupon_sum'] = 1
c6 = c6.groupby(['Merchant_id']).agg('sum').reset_index()

c7 = c[['Merchant_id','Coupon_id','Date']]
c7 = c7[(c7.Coupon_id != 'null')&(c7.Date !='null')]
c7 = c7[['Merchant_id']]
c7['merchant_coupon_used_count'] = 1
c7 = c7.groupby(['Merchant_id']).agg('sum').reset_index()
c7 = pd.merge(c6,c7,on=['Merchant_id']).reset_index()
c7.merchant_coupon_used_count = c7.merchant_coupon_used_count.replace(np.nan, 0)
c7['merchant_coupon_notuse_count'] = c7.merchant_coupon_sum - c7.merchant_coupon_used_count
c7 = c7[['Merchant_id','merchant_coupon_used_count','merchant_coupon_notuse_count']]


user_merchant1_feature = pd.merge(user_merchant1_feature, c7,on=['Merchant_id'],how='left')
user_merchant1_feature.merchant_coupon_used_count = user_merchant1_feature.merchant_coupon_used_count.replace(np.nan, 0)
user_merchant1_feature.merchant_coupon_notuse_count = user_merchant1_feature.merchant_coupon_notuse_count.replace(np.nan, 0)
user_merchant1_feature = pd.merge(user_merchant1_feature, c5,on=['User_id'],how='left')
user_merchant1_feature.user_received_coupon_use_count = user_merchant1_feature.user_received_coupon_use_count.replace(np.nan, 0)
user_merchant1_feature.user_received_coupon_notuse_count = user_merchant1_feature.user_received_coupon_notuse_count.replace(np.nan, 0)
user_merchant1_feature['user_merchant_foruser_received_coupon_notuse_rate'] = 1.0 * user_merchant1_feature.user_merchant_receivedcoupon_notuse_count / user_merchant1_feature.user_received_coupon_notuse_count
user_merchant1_feature['user_merchant_foruser_received_coupon_use_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.user_received_coupon_use_count
user_merchant1_feature['user_merchant_formerchant_received_coupon_notuse_rate'] = 1.0 * user_merchant1_feature.user_merchant_receivedcoupon_notuse_count / user_merchant1_feature.merchant_coupon_notuse_count
user_merchant1_feature['user_merchant_formerchant_received_coupon_use_rate'] = 1.0 * user_merchant1_feature.user_merchant_usecoupon_sales_count / user_merchant1_feature.merchant_coupon_used_count
user_merchant1_feature = user_merchant1_feature[['User_id','Merchant_id','user_merchant_received_coupon_count','user_merchant_sales_count',
                                                 'user_merchant_usecoupon_sales_count','user_merchant_receivedcoupon_notuse_count',
                                                 'user_merchant_usecoupon_sales_rate','user_merchant_coupon_transfer_rate',
                                                 'user_merchant_foruser_received_coupon_notuse_rate','user_merchant_foruser_received_coupon_use_rate',
                                                 'user_merchant_formerchant_received_coupon_notuse_rate','user_merchant_formerchant_received_coupon_use_rate']]
user_merchant1_feature.to_csv('characterEngineer/user_merchant1_feature.csv',index=None)
print(user_merchant1_feature.shape)


##################################拟合数据集#########################################
def get_label(s):
    s = s.split(':')
    if s[0]=='null':
        return 0
    elif (date.date(int(s[0][0:4]),int(s[0][4:6]),int(s[0][6:8]))-date.date(int(s[1][0:4]),int(s[1][4:6]),int(s[1][6:8]))).days<=15:
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
print(dataset2.shape,dataset2.columns.values.tolist())

dataset2.user_merchant_sales_count  = dataset2.user_merchant_sales_count .replace(np.nan,0)
dataset2.user_same_merchant_coupon_counts = dataset2.user_same_merchant_coupon_counts.replace(np.nan,0)
dataset2.diff_merchant_count = dataset2.diff_merchant_count.replace(np.nan,0)
dataset2['is_weekend'] = dataset2.day_of_week.apply(lambda x:1 if x in (6,7) else 0)
weekday_dummies = pd.get_dummies(dataset2.day_of_week)
weekday_dummies.columns = ['weekday'+str(i+1) for i in range(weekday_dummies.shape[1])]
dataset2 = pd.concat([dataset2,weekday_dummies],axis=1)
dataset2['label'] = dataset2.Date.astype('str') + ':' +  dataset2.Date_received.astype('str')
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
dataset1['label'] = dataset1.Date.astype('str') + ':' +  dataset1.Date_received.astype('str')
dataset1.label = dataset1.label.apply(get_label)
dataset1.drop(['Merchant_id','day_of_week','Date','Date_received','Coupon_id','coupon_count'],axis=1,inplace=True)
dataset1 = dataset1.replace('null',np.nan)
dataset1.to_csv('data/dataset1.csv',index=None)