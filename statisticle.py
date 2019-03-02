#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: statisticle.py
@author: dujiahao
@create_time: 2018/4/15 17:13
@description: 现有数据分析
"""
import pandas as pd
import tools as tool

def data_statisticler():
    "对数据进行一些统计"
    offline_train_data = pd.read_csv('data/ccf_offline_stage1_train.csv')
    # 对线下消费数据及优惠卷领取行为的一些基本统计
    # 样本数据总数
    offline_data_total = len(offline_train_data)
    print('样本数据总数:',offline_data_total)
    # 线下交易总数
    offline_total = len(offline_train_data[offline_train_data.Date != 'null'])
    print("线下交易总数:", offline_total)
    # 线下领取优惠券总数
    offline_coupons_totaldata = offline_train_data.Discount_rate
    offline_coupons_data = offline_coupons_totaldata[offline_coupons_totaldata != 'null']
    offline_coupons_total = len(offline_coupons_data)
    # 线下领取优惠券并使用 交易总数 即正样本
    offline_notnullDate_data = offline_train_data[offline_train_data.Date != 'null']
    offline_oncoupons_data = offline_notnullDate_data[offline_notnullDate_data.Coupon_id != 'null']
    offline_oncoupons_total = len(offline_oncoupons_data)
    print("线下领取优惠券并使用总数/领取优惠券总数:", offline_oncoupons_total, '/', offline_coupons_total)
    # 线下领取的满多少减多少优惠卷类型 领取数
    offline_discount_data = offline_coupons_data.values # array
    offline_coupons1_total = 0
    for x in offline_discount_data:
        if ':' in x:
            offline_coupons1_total += 1
    print('线下领取的满多少减多少优惠卷类型 领取数:',offline_coupons1_total)
    # 线下领取满多少减多少优惠卷类型并使用 总数
    offline_coupons1_usetotal = 0
    for x in offline_oncoupons_data.Discount_rate:
        if ':' in x:
            offline_coupons1_usetotal += 1
    print('线下领取满多少减多少优惠卷类型并使用 总数',offline_coupons1_usetotal)
    # 线下领取折扣率优惠卷类型 总数
    offline_coupons2_total = offline_coupons_total - offline_coupons1_total
    print('线下领取折扣率优惠卷类型 总数:',offline_coupons2_total)
    # 线下领取折扣率优惠卷类型并使用 交易总数
    offline_coupons2_usetotal = offline_oncoupons_total - offline_coupons1_usetotal
    print('线下领取折扣率优惠卷类型并使用 交易总数',offline_coupons2_usetotal)
    # 线下未领取优惠券 交易总数 即普通样本
    offline_direct_total = offline_total - offline_oncoupons_total
    print('线下未领取优惠券 交易总数 即普通样本',offline_direct_total)
    # 领取优惠券并在15天内使用 交易总数
    offline_coupons_ontimetotal = 0
    offline_onrecieve_data = (offline_oncoupons_data.Date_received).reset_index(drop = True)
    offline_onDate_data = (offline_oncoupons_data.Date).reset_index(drop = True)
    date_num = len(offline_onDate_data)
    for i in range(date_num):
        t1 = tool.handleTime(offline_onrecieve_data[i])
        t2 = tool.handleTime(offline_onDate_data[i])
        between = tool.evaluate_bteweendas(t1,t2)
        if between <= 15:
            offline_coupons_ontimetotal += 1
    print('领取优惠券并在15天内使用 交易总数', offline_coupons_ontimetotal)
    # 线下用户领取优惠券并消费的经常活动地点 总数（有活动信息的即不为null的）
    offline_notnulldistance_data = (offline_oncoupons_data[offline_oncoupons_data.Distance != 'null']).Distance
    offline_notnulldistance_total = len(offline_notnulldistance_data)
    print('线下用户领取优惠券并消费的经常活动地点 总数（有活动信息的即不为null的）',offline_notnulldistance_total)
    # 线下用户领取优惠券并消费且经常活动地点离该商家的距离低于500米 交易总数
    offline_mindistance_total = 0
    for x in offline_notnulldistance_data:
        if float(x) <= 0:
            offline_mindistance_total +=1
    print('线下用户领取优惠券并消费且经常活动地点离该商家的距离低于500米 交易总数',offline_mindistance_total)
    # 线下用户领取优惠券并消费且经常活动地点离该商家大于5公里 交易总数
    offline_maxdistance_total = 0
    for x in offline_notnulldistance_data:
        if float(x) >= 10:
            offline_maxdistance_total +=1
    print('线下用户领取优惠券并消费且经常活动地点离该商家大于5公里 交易总数',offline_maxdistance_total)
    print('-------------------------------------------------------------------------------------')
    online_train_data = pd.read_csv('data/ccf_online_stage1_train.csv')
    # 对用户线上点击/消费和优惠券领取行为的一些基本统计
    # 线上数据总数
    online_total = len(online_train_data)
    print("线上数据总数:", online_total)
    # 线上购买总数
    online_purchase_data = online_train_data[online_train_data.Action == 1]
    online_purchase = len(online_purchase_data)
    print('线上购买总数', online_purchase)
    # 线上领取优惠券总数
    online_receivecoupons_data = online_train_data[online_train_data.Action == 2]
    online_coupons_total = len(online_receivecoupons_data)
    print('线上领取优惠券总数', online_coupons_total)
    # 线上领取满多少减多少优惠券 总数
    online_coupons1_total = 0
    for x in online_receivecoupons_data.Discount_rate:
        if ':' in x:
            online_coupons1_total += 1
    print('线上领取满多少减多少优惠券 总数', online_coupons1_total)
    # 线上领取低价限时优惠券 总数
    online_fixed_total = 0
    for x in online_train_data.Coupon_id:
        if x == 'fixed':
            online_fixed_total += 1
    print('线上开展低价限时活动 总数', online_fixed_total)
    # 线上领取折扣率优惠券 总数
    online_coupons2_total = 0
    print('线上领取折扣率优惠券 总数', online_coupons2_total)

    # 线上使用优惠券消费 总数
    online_oncoupons_data =  online_purchase_data [ online_purchase_data.Coupon_id != 'null']
    online_oncoupons_total = len( online_oncoupons_data)
    print('线上使用优惠券消费 总数', online_oncoupons_total)
    # 线上领取优惠券并使用的时间跨度小于15天 交易总数
    online_coupons_usetotal = 0
    online_receive_data = (online_oncoupons_data.Date_received).reset_index(drop = True)
    online_spend_date = (online_oncoupons_data.Date).reset_index(drop = True)
    online_date_num = len(online_spend_date)
    for i in range(online_date_num):
        t1 = tool.handleTime(online_receive_data[i])
        t2 = tool.handleTime(online_spend_date[i])
        bet = tool.evaluate_bteweendas(t1, t2)
        if bet <= 15 :
            online_coupons_usetotal += 1
    print('线上领取优惠券并使用的时间跨度小于15天 交易总数', online_coupons_usetotal)
    # 线上未领取优惠券并消费 交易总数
    online_normal_data = online_purchase_data[online_purchase_data.Coupon_id == 'null']
    online_nncoupons_total = len(online_normal_data)
    print('线上未领取优惠券并消费 交易总数', online_nncoupons_total)


data_statisticler()



"""
样本数据总数: 1,754,884
线下交易总数: 776，984


线下领取优惠券并使用总数/领取优惠券总数: 75，382 / 1，053，282
线下领取的满多少减多少优惠卷类型 领取数: 1，020，010
线下领取满多少减多少优惠卷类型并使用 总数 71，529
线下领取折扣率优惠卷类型 总数: 3，3272
线下领取折扣率优惠卷类型并使用 交易总数 3，853
线下未领取优惠券 交易总数 即普通样本 701，602
领取优惠券并在15天内使用 交易总数 64，872
线下用户领取优惠券并消费的经常活动地点 总数（有活动信息的即不为null的） 67，165
线下用户领取优惠券并消费且经常活动地点离该商家的距离低于500米 交易总数 46,852
线下用户领取优惠券并消费且经常活动地点离该商家大于5公里 交易总数 2,496
-------------------------------------------------------------------------------------
线上数据总数: 11,429,826
线上购买总数 1,372,148
线上领取优惠券总数 655,898
线上领取满多少减多少优惠券 总数 655,898
线上开展低价限时活动 总数 131,546
线上领取折扣率优惠券 总数 0
线上使用优惠券消费 总数 216,459
线上领取优惠券并使用的时间跨度小于15天 交易总数 212,977
线上未领取优惠券并消费 交易总数 1,155,689

"""