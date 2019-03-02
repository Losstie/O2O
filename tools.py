#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: tools.py
@author: dujiahao
@create_time: 2018/4/14 11:16
@description: 工具函数
"""
import pandas as pd
import time
def handleTime(timeStr,formats='%Y%m%d'):
    "处理时间字符串 返回时间元组"
    t = time.strptime(timeStr, formats)

    return t
def judege_leapyear(year):
    "判断是否为闰年 "
    if year%4 == 0:
        if year % 100 != 0:
            mark = True
        else:
            mark = False
    elif year % 400 == 0:
        mark = True
    else:
        mark =  False

    return mark
def evaluate_bteweendas(date1,date2):
    "计算日期之间间隔天数"
    leapyear = pd.Series([31,29,31,30,31,30,31,31,30,31,30,31], index= [1,2,3,4,5,6,7,8,9,10,11,12])
    leapyear_total = 366
    non_leapyear = pd.Series([31,28,31,30,31,30,31,31,30,31,30,31], index= [1,2,3,4,5,6,7,8,9,10,11,12])
    non_leapyear_total = 365
    date1_totaldays = 0
    date2_totaldays = 0
    # 计算date1已经在该年度过多少天
    if judege_leapyear(date1.tm_year):
        for i in range(date1.tm_mon):
            date1_totaldays += leapyear[i+1]
    else:
        for i in range(date1.tm_mon):
            date1_totaldays += non_leapyear[i+1]
    date1_totaldays += date1.tm_mday
    # 计算date2已经在该年度过多少天
    if judege_leapyear(date2.tm_year):
        for i in range(date2.tm_mon):
            date2_totaldays += leapyear[i + 1]
    else:
        for i in range(date2.tm_mon):
            date2_totaldays += non_leapyear[i + 1]
    date2_totaldays += date2.tm_mday
    days = 0
    # 判断两日期是否为同一年并做出处理
    if date1.tm_year == date2.tm_year:
        days = abs(date1_totaldays - date2_totaldays)
    else:
        if date1.tm_year < date2.tm_year:
            days += date2_totaldays
            for i in range(date2.tm_year - date1.tm_year):
                if i == 0:
                    if judege_leapyear(date1.tm_year):
                        days += leapyear_total - date1_totaldays
                    else:
                        days += non_leapyear_total - date1_totaldays
                else:
                    if judege_leapyear(date1.tm_year + i):
                        days += leapyear_total
                    else:
                        days += non_leapyear_total
        else:
            days += date1_totaldays
            for i in range(date1.tm_year - date2.tm_year):
                if i == 0:
                    if judege_leapyear(date2.tm_year):
                        days += leapyear_total - date2_totaldays
                    else:
                        days += non_leapyear_total - date2_totaldays
                else:
                    if judege_leapyear(date2.tm_year + i):
                        days += leapyear_total
                    else:
                        days += non_leapyear_total
    return days




