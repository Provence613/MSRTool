import datetime
import os
import pandas as pd
import csv

from MutantSetReduce.FeatureConverse import FeatureConverse
from MutantSetReduce.QualityScorePredict import QualityScorePredict
from MutantSetReduce.MSReduceForGA import MSReduceForGA
from MutantSetReduce.ResultProcess import ResultProcess

'''
author:liufangxiao
description:mutant set reduction
'''
def main(projectName,hasModel,boundarylist=[4,6]):
    srcfilename = projectName + '.csv'
    srcfile = os.path.join('D:/mutationtestingReduction/MSReduction/output', srcfilename)
    optfilename = projectName + 'Data.csv'
    optfile = os.path.join('D:/mutationtestingReduction/MSReduction/output', optfilename)
    modelname = 'rfmodel_' + projectName + '.pkl'
    modelpath = os.path.join("D:/mutationtestingReduction/MSReduction/output", modelname)
    reduceResName = 'mutantreduce_' + projectName + '.csv'
    reduceRespath = os.path.join("D:/mutationtestingReduction/MSReduction/output", reduceResName)
    reduceResjsonName = 'mutantreduce_' + projectName + '.json'
    reduceResjsonpath = os.path.join("D:/mutationtestingReduction/MSReduction/output", reduceResjsonName)

    max_iter = 10
    populationSize = 50
    # 预处理
    df = pd.read_csv(srcfile, delimiter=",", quoting=csv.QUOTE_NONE, encoding='utf-8')
    # 去掉重复行
    df = df.drop_duplicates()
    df.to_csv(srcfile, index=False, header=True)
    if(not hasModel):
        # 特征转变
        fc = FeatureConverse()
        fc.process_data(srcfile, optfile)

        # qsp预测
        qsp = QualityScorePredict()
        # model_compare()
        qsp.train_rfrmodel(optfile, modelpath)
        # train_xgbmodel()
        # crossproject()

    # ms约简
    msr = MSReduceForGA()
    solution, value, size, df = msr.run(srcfile, modelpath, boundarylist,max_iter, populationSize)
    mutantSize,mscore,testSize=msr.outputRes(solution, value, size, df, reduceRespath)
    # 约简结果转换
    rp = ResultProcess()
    rp.conversefile(reduceRespath, reduceResjsonpath)
    return mutantSize,mscore,testSize
# if __name__ == '__main__':
#     starttime = datetime.datetime.now()
#     # projectName = "exp4j"
#     projectName="msgpack"
#     main(projectName,False)
#     endtime = datetime.datetime.now()
#     print("Time of reducing mutant set",(endtime - starttime).seconds)
    # exp4j 329s all