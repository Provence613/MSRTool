import os
import timeit
import datetime

from TestDataProcess.Analyzer import Analyzer
from TestDataProcess.MutantGen import MutantGen
from TestDataProcess.ProjectConfig import ProjectConfig
from TestDataProcess.ExecutedInfoGen import ExecutedInfoGen
from TestDataProcess.CoveredInfoGen import CoveredInfo
from TestDataProcess.ClassAssertGen import ClassAssertGen
from TestDataProcess.MethodAssertGen import MethodAssertGen
from TestDataProcess.StaticMetricGen import StaticMetricGen
from TestDataProcess.TestReportAnalyzer import TestReportAnalyzer

'''
author:liufangxiao
description:test data processor
'''

def featureExtract(roorDir,outputpath):
    analyzer = Analyzer(roorDir)
    analyzer.setMutantKilling()
    analyzer.setNumCovered()
    analyzer.setClassAssert()
    analyzer.analyzeTestMethodResult()
    analyzer.analyzeCoverage()
    analyzer.setNumTestsCover()
    analyzer.setNumAssert()
    analyzer.analyzeStaticMetric()
    analyzer.setStaticMetric()
    analyzer.outputFeature(outputpath)
def projectconfig(projectdir):
    p=ProjectConfig()
    p.projectStart(projectdir)
def mutantGenerate(projectdir,pitdir,desdir):
    m = MutantGen()
    m.mutantGen(projectdir)
    m.copy_file(pitdir,desdir)
    m.parseXML(desdir)
def testexecutedInfoGenerate(projectdir,coberturafile,desdir):
    e=ExecutedInfoGen()
    e.executedInfoGen(projectdir)
    e.copy_file(coberturafile,desdir)
def testreportanalyer(desdir):
    t = TestReportAnalyzer()
    t.parseHtml(desdir)
def testcoveredInGenerate(projectdir,desdir):
    c = CoveredInfo()
    c.coveredInfoGen(projectdir)
    srcfilepath=os.path.join(projectdir, "stmt-cov.txt")
    c.copy_file(srcfilepath,desdir)
    c.parse(desdir)
def classassetInfoGenerate(projectdir,desdir):
    testpath = os.path.join(projectdir, "src/test")
    classpath = os.path.join(projectdir, "src/main")
    c=ClassAssertGen(testpath,classpath,desdir)
    c.classassertInfoGen()
def methodassetInfoGenerate(projectdir,desdir):
    testpath = os.path.join(projectdir, "src/test")
    m=MethodAssertGen(testpath,desdir)
    m.methodassertGen()
def staticMetricInfoGenerate(toolpath,projectdir,desdir):
    s=StaticMetricGen()
    s.staticmetricGen(toolpath,projectdir,desdir)
    s.parseHtml(desdir)

def main(projectName,projectdir,pitdir,coberturadir):
    srcdir = 'D:/mutationtestingReduction/MSReduction/sourcecode'
    optdir = 'D:/mutationtestingReduction/MSReduction/output'
    toolpath = "D:/mutationtestingReduction/MSReduction/tools/jhawkCommandLine"

    rootdir = os.path.join(srcdir, projectName)
    # 判断路径是否存在
    if not os.path.exists(rootdir):
        os.makedirs(rootdir)
    outputpath = os.path.join(optdir, projectName + ".csv")

    # 项目初始化 mvn clean
    projectconfig(projectdir)
    # 测试覆盖信息生成 mvn test
    testcoveredInGenerate(projectdir, rootdir)
    # 变异信息生成
    mutantGenerate(projectdir, pitdir, rootdir)
    # 测试执行信息生成
    testexecutedInfoGenerate(projectdir, coberturadir, rootdir)
    # class断言信息生成
    classassetInfoGenerate(projectdir, rootdir)
    # method断言信息生成
    methodassetInfoGenerate(projectdir, rootdir)
    # 静态信息生成
    staticMetricInfoGenerate(toolpath, projectdir, rootdir)
    # 覆盖测试报告生成
    testreportanalyer(rootdir)
    # 特征提取
    featureExtract(rootdir, outputpath)


# if __name__ == '__main__':
#     starttime = datetime.datetime.now()
#     projectName = "exp4j"
#     projectdir = "D:/mutationtestingReduction/expData/exp4j-exp4j-0.4.8"
#     pitdir = "D:/mutationtestingReduction/expData/exp4j-exp4j-0.4.8/target/pit-reports/"
#     coberturadir = "D:/mutationtestingReduction/expData/exp4j-exp4j-0.4.8/target/site/cobertura"
#     main(projectName,projectdir,pitdir,coberturadir)
#     # 测量运行时间
#     endtime = datetime.datetime.now()
#     print('Time of Feature Extracting Elapsed:(S)',(endtime - starttime).seconds)









