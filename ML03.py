# -*- coding: utf-8 -*-
# モデルの保存
# APIなどで利用する際はjoblib.loadで保存したモデルを読み込んで、
# 入力されたデータに対してpredictを行えば良い
import numpy as np
from ML04 import get_stock
import pandas as pd
from sklearn import tree
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# リターンインデックス
def get_ret_index(close):
    # データーが昇順（日付が過去が上になって最新が一番下）になっている前提
    returns = pd.Series(close).pct_change() # 騰落率を求める
    ret_index = (1 + returns).cumprod() # 累積積を求める
    ret_index.iloc[0] = 1 # 最初の値を 1.0 にする
    return ret_index

# 学習データーの作成
def train_data(arr, step):
    train_X = []
    train_y = []

    for i in range(0, len(arr) - step):
        end = i + step
        data = arr.iloc[i:end]
        feature = get_ret_index(arr)
        if feature.iloc[-1] < arr.iloc[end]: # その翌日、株価は上がったか？
            # 上がっていれば１
            res = 1
        else:
            # 下がっていれば０
            res = 0
        train_X.append(feature.values)
        train_y.append(res)
    return np.array(train_X), np.array(train_y)

#return 教師データ配列、対応１か０かのラベル
def train_data2(arr):
    train_x=[]
    train_y=[]

    #30日間のデータを学習、1日ずつ後ろにずらしていく
    for i in range(-len(arr),-15):
        s = i+14 #14日間の変化を素数にする
        feature = arr[i:s].values
        if feature[-1] < arr[s]:#その翌日、株価は上がったか？
            train_y.append(1) #yes
        else :
            train_y.append(0) #no
        train_x.append(feature)
    return np.array(train_x),np.array(train_y)

def main():
    code=6641 #日新電機
    
    # 株価の取得(銘柄コード, 開始日)
    #fromDate ='2017-1-1'
    #df = get_stock(code, fromDate)
    df = pd.read_csv('{}.csv'.format(code))
    
    train_x, train_y = train_data(df.close[:100], 10)
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_x, train_y)
    test_x, test_y = train_data(df.close.tail(10), 10)
    result = clf.predict(test_x)
    
    print('test_y:{}'.format(test_y))
    print('result:{}'.format(result))
    
if __name__ == "__main__":
    main()

