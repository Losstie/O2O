#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@project: FinaDesigner_Dujiahao
@file: main.py
@author: dujiahao
@create_time: 2018/4/14 10:58
@description: 主函数
"""
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
import xgboost as xgb
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
# 程序开始时间
start_time = time.time()

# XgBoost 参数
params = {'booster': 'gbtree',
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

history_auc = []
history_n = []

def callback_draw(env):
    # "用于每次迭代结束时候刷新auc变化曲线"
    result_list = env.evaluation_result_list
    n_rounds = env.iteration + 1
    score = result_list[0][1]

    if(len(history_auc) > 10):
        plt.close('all')

    if(n_rounds % 10 == 0):
        print(n_rounds)
        history_auc.append(score)
        history_n.append(n_rounds)
        # if (len(history_auc) >= 150):
        #     del history_auc[0]
        #     del history_n[0]
        plt.plot(np.array(history_n),np.array(history_auc))
        plt.show()

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
    # 划分出验证集调参数   找出最优参数
    # x_dtrain, x_deval, y_dtrain, y_deval = train_test_split(dataset12_x, dataset12_y, random_state=1000,test_size=0.3)
    # train = xgb.DMatrix(x_dtrain,y_dtrain)
    # deval = xgb.DMatrix(x_deval,y_deval)
    #
    # dataset3 =  xgb.DMatrix(dataset3_x)
    # watchlist = [(deval,'eval')]
    # model = xgb.train(params, train, num_boost_round=500, evals=watchlist,early_stopping_rounds=30)

    # 找出参数后  将两数据集合并进行训练 以达到最优

    dataset1 = xgb.DMatrix(dataset1_x, label=dataset1_y)
    dataset2 = xgb.DMatrix(dataset2_x, label=dataset2_y)
    dataset12 = xgb.DMatrix(dataset12_x, label=dataset12_y)
    dataset3 = xgb.DMatrix(dataset3_x)
    # watchlist = [(dataset12,'train')]
    # model = xgb.train(params, dataset12, num_boost_round=4000, evals=watchlist,early_stopping_rounds=120)
    # model.save_model('xgb.model')

    # 可视化
    # 绘制特征重要性条形图
    # fig, ax = plt.subplots()
    # fig.set_size_inches(24, 12)
    # xgb.plot_importance(model,height=0.5,ax=ax)
    # plt.show()
    #
    # # 绘制决策树
    # fig, ax = plt.subplots()
    # fig.set_size_inches(60, 30)
    # xgb.plot_tree(model,ax=ax)
    # plt.show()
    #
    # import codecs
    # f = codecs.open('xgb_tree.png', mode='wb')
    # g = xgb.to_graphviz(model)
    # f.write(g.pipe('png'))
    # f.close()

    # predict test set

    model = xgb.Booster(model_file='xgb.model')
    dataset3_preds['label'] = model.predict(dataset3)
    dataset3_preds.label = MinMaxScaler().fit_transform(dataset3_preds.label.reshape(-1, 1))
    dataset3_preds.sort_values(by=['Coupon_id', 'label'], inplace=True)
    dataset3_preds.to_csv("xgb_preds.csv", index=None, header=None)
    print(dataset3_preds.describe())

    # save feature score
    # feature_score = model.get_fscore()
    # feature_score = sorted(feature_score.items(), key=lambda x: x[1], reverse=True)
    # fs = []
    # for (key, value) in feature_score:
    #     fs.append("{0},{1}\n".format(key, value))
    #
    # with open('xgb_feature_score.csv', 'w') as f:
    #     f.writelines("feature,score\n")
    #     f.writelines(fs)
    # 程序运行时间
    cost_time = time.time() - start_time
    print("cost_time:", cost_time)
