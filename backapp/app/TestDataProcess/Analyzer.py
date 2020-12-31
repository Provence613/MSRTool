from TestDataProcess.Mutant import Mutant
from TestDataProcess.ClassAssertAnalyzer import ClassAssertAnalyzer
from TestDataProcess.Utils import Utils
from TestDataProcess.CoberturaAnalyzer import CoberturaAnalyzer
from TestDataProcess.FeatureOutput import FeatureOutput
import os
import csv

class Analyzer:
    mutants=[]
    methodAssertDic = {}
    mutantMethodDic={}
    staticmetricDic={}

    def __init__(self,rootDir=None,metrics=None,delimiter=None):
        self.rootDir = rootDir
        self.metrics = metrics
        self.delimiter = delimiter

    # 初始化变异体
    def setMutantKilling(self):
        path = os.path.join(self.rootDir, "mutInfoC.csv")
        index=0
        # 变异体数组
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for mutation in reader:
                if index==0:
                    index+=1
                    continue
                # print(mutation)
                fullname=mutation[4].lower()
                # if fullname.find("$")>=0:
                #     idx=fullname.find("$")
                #     fullname=fullname[0:idx]
                lineNumber=mutation[7]
                javaFileName=fullname+'.java'
                methodName=mutation[5].lower()
                status=mutation[0]
                if status=="KILLED":
                    mutant=Mutant(fullname,lineNumber,javaFileName,methodName,status)
                    self.mutants.append(mutant)
                    setattr(mutant,mutant.FULLCLASS,fullname)
                    setattr(mutant, mutant.FULLMETHOD, fullname+'.'+methodName)
                    setattr(mutant,mutant.KEY,fullname+'.'+methodName+":"+lineNumber)
                    setattr(mutant,mutant.OPERATOR,mutation[8])
                    methodReturn = mutation[6]
                    if methodReturn.startswith("L") or methodReturn.startswith("[L") or methodReturn.startswith("[[L"):
                        methodReturn= "method"
                    setattr(mutant,mutant.METHODRETURN,methodReturn)
                    setattr(mutant, mutant.KILLTEST, mutation[9])
                    setattr(mutant,mutant.ROWNUM,lineNumber)
                    setattr(mutant,mutant.ISKILLED,mutation[1])
    # 设置CLASSASSERT特征
    def setClassAssert(self):
        classassertAnalyzer = ClassAssertAnalyzer()
        classassertAnalyzer.analyzer(self.rootDir,self.mutants)
        # for mutant in self.mutants:
            # print(getattr(mutant,mutant.CLASS_ASSERT))

    def analyzeTestMethodResult(self):
        path = os.path.join(self.rootDir, "testMethodResult.txt")
        f = open(path, "r")
        lines = f.readlines()

        fullClassName=None
        for line in lines:
            if len(line.strip())==0:
                fullClassName=None
                continue
            if fullClassName==None:
                utils = Utils()
                fullClassName = utils.getClassNameFromDir(line)
            else:
                try:
                    fullMethodName=fullClassName+':'+line.split(",")[1].split("(")[0].lower()
                    num = int(line.split(",")[-1])
                    oldNum = self.methodAssertDic.get(fullMethodName)
                    if oldNum != None and oldNum != num:
                        num = oldNum + num
                    self.methodAssertDic[fullMethodName] = num
                except:
                    print("ERROR"+line)
                # num=int(line.split(",")[-1])
                # oldNum=self.methodAssertDic.get(fullMethodName)
                # if oldNum!=None and oldNum!=num:
                #     num=oldNum+num
                # self.methodAssertDic[fullMethodName]=num
        # print(self.methodAssertDic)
        # print(len(self.methodAssertDic))

    def analyzeCoverage(self):
        path = os.path.join(self.rootDir, "coverage.txt")
        f = open(path, "r")
        lines = f.readlines()
        for line in lines:
            ele=line.split("=")
            mutantFullInfo = ele[0].split(":")
            class_name = mutantFullInfo[0].replace("/", ".")
            mutantID = (class_name + ".java").lower() + ":" + mutantFullInfo[1]
            # print(mutantID)
            innerMap=self.mutantMethodDic.get(mutantID)
            if innerMap==None:
                innerMap={}
            self.mutantMethodDic[mutantID]=innerMap
            methods=[]
            if(len(ele[1])>1):
                methods=ele[1][1:-2].split(",")
            for string in methods:
                mName=string.lower()
                num=self.methodAssertDic.get(mName)
                if num==None:
                    num=0
                innerMap[mName]=num
        # print(len(self.mutantMethodDic))
    # 设置NUMTESTCOVERED特征
    def setNumTestsCover(self):
        for mutant in self.mutants:
            idName =getattr(mutant,"javaFileName")+":"+getattr(mutant,mutant.ROWNUM)
            innerMap=self.mutantMethodDic.get(idName)
            if innerMap==None:
                setattr(mutant,mutant.NUMTESTSCOVER,"0")
            else:
                setattr(mutant, mutant.NUMTESTSCOVER, len(innerMap))
            # print(getattr(mutant,mutant.NUMTESTSCOVER))
    # 设置NUMASSERT特征
    def setNumAssert(self):

        for mutant in self.mutants:
            idName =getattr(mutant,"javaFileName")+":"+getattr(mutant,mutant.ROWNUM)
            innerMap=self.mutantMethodDic.get(idName)
            if innerMap==None:
                setattr(mutant,mutant.NUM_ASSERT,"0")
            else:
                val=0
                for key in innerMap:
                    val+=int(innerMap[key])
                setattr(mutant, mutant.NUM_ASSERT, str(val))
            # print(getattr(mutant,mutant.NUM_ASSERT))
    # 设置NUMCOVERED特征
    def setNumCovered(self):
        c = CoberturaAnalyzer()
        c.analyze(self.rootDir,self.mutants)
    def analyzeStaticMetric(self):
        path = os.path.join(self.rootDir, "staticMetrics.csv")
        index = 0
        # 变异体数组
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for metrics in reader:
                if index==0:
                    index+=1
                    continue
                fullmethodName=(metrics[0]+'.'+metrics[1]+'.java:'+metrics[2]).lower()
                # print(fullmethodName)
                self.staticmetricDic[fullmethodName]=metrics[3:]
                # print(len(self.staticmetricDic[fullmethodName]))

    #设置静态特征
    def setStaticMetric(self):
        for mutant in self.mutants:
            idName = getattr(mutant, "javaFileName") + ":" + getattr(mutant,"methodName")
            # print(idName)
            metrics = self.staticmetricDic.get(idName)
            features = ["mmCOMP", "mmNOCL", "mmNOS", "mmHLTH", "mmHVOC", "mmHEFF", "mmHBUG", "mmCREF", "mmXMET", "mmLMET", "mmNLOC", "mmNOC", "mmNOA", "mmMOD", "mmHDIF", "mmVDEC", "mmEXCT", "mmEXCR", "mmCAST", "mmTDN", "mmHVOL", "mmNAND", "mmVREF", "mmNOPR", "mmMDN", "mmNEXP", "mmLOOP",
        "ccNoMethods", "ccLCOM", "ccAVCC", "ccNOS", "ccHBUG", "ccHEFF", "ccUWCS", "ccINST", "ccPACK", "ccRFC", "ccCBO", "ccMI", "ccCCML", "ccNLOC", "ccRVF", "ccF-IN", "ccDIT", "ccMINC", "ccS-R", "ccR-R", "ccCOH", "ccLMC", "ccLCOM2", "ccMAXCC", "ccHVOL", "ccHIER", "ccNQU", "ccFOUT", "ccSuperclass", "ccSIX", "ccEXT", "ccNSUP", "ccTCC", "ccNSUB", "ccMPC", "ccNCO", "ccINTR", "ccCCOM", "ccHLTH", "ccMOD",
        "ppNoClasses", "ppNOS", "ppAVCC", "ppHBUG", "ppHEFF", "ppHLTH", "ppHVOL", "ppMI", "ppCCML", "ppNLOC", "ppRVF", "ppTCC", "ppCCOM", "ppINST", "ppDIST", "ppFIN", "ppNoMethods", "ppMINC", "ppABST", "ppMAXCC", "ppFOUT"]
            if metrics==None:
                for feature in features:
                    setattr(mutant,feature,None)
            else:
                i=0
                # print(idName)
                # print(len(metrics))
                for feature in features:
                    setattr(mutant, feature, metrics[i])
                    i+=1
            # print(getattr(mutant,"mmCOMP"))
    def outputFeature(self,path):
        f=FeatureOutput()
        f.mutantToFile(path,self.mutants)








