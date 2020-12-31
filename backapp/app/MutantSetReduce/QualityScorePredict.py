import pandas as pd
import os
import math
import numpy as np
from math import log10

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import cross_validate
import pickle

class QualityScorePredict:
    # 数据处理
    def process_data(self,filename):
        # 读文件
        df = pd.read_csv(filename)
        # df.drop(['Unnamed: 0'], axis=1)
        print(df.describe())                #各项统计
        # print(df.info())                      #看总数及数值类型
        # print(list(df.columns))         #获取列名（以list形式返回）
        # 处理特征
        featuresTwo=['numCovered','numTestsCover','mutantAssert','classAssert']
        for feature in list(df.columns):
            arr=df[feature].values.tolist()
            for i in range(len(arr)):
                if feature!="isKilled":
                    if feature in featuresTwo and float(arr[i]) > 1.0:
                        arr[i] = log10(float(arr[i])) / log10(1.2)
                    else:
                        arr[i]=float(arr[i])
            df[feature] = pd.DataFrame(arr)

        # 划分训练集 and 测试集
        #data:需要进行分割的数据集
        #random_state:设置随机种子，保证每次运行生成相同的随机数
        #test_size:将数据分割成训练集的比例
        x, y = df.iloc[:, 1:-1].values, df.iloc[:, -1].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        # train_set.to_csv("../Data/train_set.csv")
        # test_set.to_csv("../Data/test_set.csv")
        # print(type(x))
        # print(type(x_train))
        return x_train, x_test, y_train, y_test,list(df.columns)
    def print_score(self,m,modelname,x_train, x_test, y_train, y_test):
        # print( m.MutantSetReduce(x_test))
        if modelname in ['Random Forest', 'Linear', 'SVR']:
            print(modelname+"的模型评估值为："+str(m.score(x_train, y_train)))
            print(modelname+"的默认评估值为："+str(m.score(x_test, y_test)))
        print(modelname+"的R_squared值为："+str(r2_score(y_test, m.predict(x_test))))
        print(modelname+"的均方误差rmse为:"+str(math.sqrt(mean_squared_error(y_test, m.predict(x_test)))))
        print(modelname+"的平均绝对误差mae为:"+str(mean_absolute_error(y_test, m.predict(x_test))))
    def kfoldValidation(self,k,filename):
        x,y=self.processData4kfold(filename)
        rf = RandomForestRegressor(n_estimators=20, max_features=0.5, random_state=42, n_jobs=-1)
        scoring = ['neg_mean_absolute_error', 'neg_mean_squared_error','r2']  # 设置评分项
        scores = cross_validate(rf, x, y, scoring=scoring, cv=k, return_train_score=False)
        print(scores)
        print(scores['test_r2'])
        print(np.mean(scores['test_r2']))
    def train_rfrmodel(self,filepath,modelpath):
        x_train, x_test, y_train, y_test,features=self.process_data(filepath)
        names=features[1:-1]
        # print(names)
        rf = RandomForestRegressor(n_estimators=20, max_features=0.5, random_state=42, n_jobs=-1)
        rf.fit(x_train, y_train)

        with open(modelpath, "wb") as f:
            pickle.dump(rf, f)
        self.print_score(rf,"随机森林回归",x_train, x_test, y_train, y_test)
        feat_importances = pd.Series(rf.feature_importances_, index=names)
        feat_importances.sort_values(ascending=False, inplace=True)
        print("特征重要性：")
        print(feat_importances)
    
    # 项目间实验
    def crossproject(self,modelpath,filepath):
        # "../MutantSetReduce/rfmodel_lang.pkl"
        with open(modelpath, "rb") as f:
            model = pickle.load(f)
            # "../Data/commonsTextData.csv"
            x_train, x_test, y_train, y_test, features = self.process_data(filepath)
            model.fit(x_train, y_train)
            self.print_score(model, "随机森林回归", x_train, x_test, y_train, y_test)


