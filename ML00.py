# -*- coding: utf-8 -*-
#機器学習原理：
#①線形計算式
# y =W0 + W1x1 + W2x2 + W3x3 + ...Wnxn
"""
    code = 6641 #
    fromDate ='2015-1-1'
    df = get_stock(code, fromDate, datetime.date.today())

    %run in ipython
    import os
    filepath='C:\\Users\\User\\FolderWithPythonScript' 
    os.chdir(filepath)
    %run pyFileInThatFilePath.py
"""

#from sklearn.datasets import load_digits                        #テストデータ引用
#from sklearn.cross_validation import train_test_split           #テストデータの分割
from sklearn.svm import LinearSVC                               #評価機の導入
from sklearn.metrics import confusion_matrix, accuracy_score    #
from sklearn.externals import joblib

#学習データの準備.
#一行データは一回のｘ1～Xn値により計算。
xtrainData = [[1,1,1,1,1], [2,2,2,2,2], [3,3,3,3,3]]

#3行データの三回計算結果
xtrainLabel= [6,11,16]

#scikit.learnにSVMは SVC, LinearSVC, NuSVC三種類有ります。
estimator = LinearSVC() #SVCはもう一つ種類の評価機

#トレーニングデータで学習を実施
#機器学習により専用評価原理の確定
estimator.fit(xtrainData, xtrainLabel)

# モデルの保存
# APIなどで利用する際はjoblib.loadで保存したモデルを読み込んで、
# 入力されたデータに対してpredictを行えば良い
joblib.dump(estimator, 'estimator.pkl') 

#評価データの準備
xtestData = [[4,4,4,4,4]]

#テストデータで予測
predict_label = estimator.predict(xtestData)

test_label= [16]

#結果評価
result = confusion_matrix(test_label, predict_label)
score =  accuracy_score  (test_label, predict_label)

#結果出力
print ('\n★predict_label:{} ,test_label:{}, result:{}, score:{},'.format(predict_label,test_label,result, score))
