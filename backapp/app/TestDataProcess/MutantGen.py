import os
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom
import csv
import json

class MutantGen:
    # 变异生成
    def mutantGen(self, path):
        print('测试开始')
        # os.chdir(path)
        # print(os.popen('mvn org.pitest:pitest-maven:mutationCoverage').read())
        # try:
        #     os.chdir(path)
        #     info = os.popen('mvn org.pitest:pitest-maven:mutationCoverage').read()
        #     # 触发异常
        #     if (info.find('BUILD FAILURE') >= 0):
        #         # 将错误信息传递给用户
        #         raise Exception(info)
        #     else:
        #         # 打印输出，方便开发者了解运行进度
        #         print(info)
        # except Exception as e:
        #     print('Error in mutant generation')
        #     print(e)
        #     # 因为出现错误，所以非正常退出，后面语句不执行了
        #     exit(1)
        os.chdir(path)
        info = os.popen('mvn org.pitest:pitest-maven:mutationCoverage').read()
        # 触发异常
        if (info.find('BUILD FAILURE') >= 0):
            # 将错误信息传递给用户
            raise Exception(info)
        else:
            # 打印输出，方便开发者了解运行进度
            print(info)
        print('测试结束')
    # 变异信息转储
    def copy_file(self,srcDir, desDir):
        dir = os.listdir(srcDir)[0]
        dirpath = os.path.join(srcDir, dir)
        ls=os.listdir(dirpath)
        for line in ls:
            filePath = os.path.join(dirpath, line)
            if os.path.isfile(filePath):
                print(filePath)
                shutil.copy(filePath, desDir)
    # 解析变异信息
    def parseXML(self,dir):
        xmlpath = os.path.join(dir, "mutations.xml")
        DOMTree = xml.dom.minidom.parse(xmlpath)
        collection = DOMTree.documentElement
        # 在集合中获取所有mutant
        mutations = collection.getElementsByTagName("mutation")
        allMutants=[]
        allMutantsList=[]
        i=1
        for mutation in mutations:
            mutant=[]
            mutantdic={}
            mutantdic['id']=i
            status = mutation.getAttribute("status")
            mutant.append(status)
            isKilled = mutation.getAttribute("detected")
            mutant.append(isKilled)
            numberOfTestsRun = mutation.getAttribute("numberOfTestsRun")
            mutant.append(numberOfTestsRun)
            sourceFile = mutation.getElementsByTagName('sourceFile')[0].childNodes[0].data
            # print(sourceFile.childNodes[0].data)
            mutant.append(sourceFile)
            mutatedClass= mutation.getElementsByTagName('mutatedClass')[0].childNodes[0].data
            # print(mutatedClass.childNodes[0].data
            mutantdic['ClassName']=mutatedClass
            mutant.append(mutatedClass)
            mutatedMethod= mutation.getElementsByTagName('mutatedMethod')[0].childNodes[0].data
            mutant.append(mutatedMethod)
            mutantdic['MethodName']=mutatedMethod
            # print(mutatedMethod.childNodes[0].data)
            methodDescription= mutation.getElementsByTagName('methodDescription')[0].childNodes[0].data.split(')')[-1]
            mutant.append(methodDescription)
            # print(methodDescription.childNodes[0].data)
            lineNumber = mutation.getElementsByTagName('lineNumber')[0].childNodes[0].data
            mutant.append(lineNumber)
            mutantdic['RowNumber']=lineNumber
            # print(lineNumber.childNodes[0].data)
            mutator= mutation.getElementsByTagName('mutator')[0].childNodes[0].data.split('.')[-1]
            # print(mutator.childNodes[0].data)
            mutant.append(mutator)
            mutantdic['Operator']=mutator
            killingTest = mutation.getElementsByTagName('killingTest')[0]
            if len(killingTest.childNodes)!=0:
                mutant.append(killingTest.childNodes[0].data.split('(')[0])
            else:
                mutant.append('')
            description = mutation.getElementsByTagName('description')[0].childNodes[0].data
            mutant.append(description)
            # mutantdic['Detail']=description
            # print(mutant)
            allMutants.append(mutant)
            allMutantsList.append(mutantdic)
            i+=1

        # 写入csv
        outputpath = os.path.join(dir, "mutInfoC.csv")
        with open(outputpath, "w",newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(["isKilled","status","numberOfTestsRun","sourceFile","mutatedClass","mutatedMethod","methodDescription","lineNumber","mutator","killingTest","description"])
            # 写入多行用writerows
            writer.writerows(allMutants)
        # 写入json
        jsondic={}
        jsondic['results']=allMutantsList
        jsonpath = os.path.join(dir, "mutantInfo.json")
        file = open(jsonpath, 'w', encoding='utf-8')
        json.dump(jsondic, file, ensure_ascii=False)
        file.close()
    def getMutInfo(self,results,page,filename):
        startId=(page-1)*results
        endId=startId+results
        with open(filename, 'r') as f:
            data = json.load(f)
            res=data['results']
            jsondic = {}
            newres=[]
            for i in range(startId,endId):
                newres.append(res[i])
            jsondic['results']=newres
            print(json.dumps(jsondic, ensure_ascii=False))
            # print()

# m=MutantGen()
#  m.parseXML('D:/mutationtestingReduction/MSReduction/sourcecode/exp4j')
# m.getMutInfo(10,3,'D:/mutationtestingReduction/MSReduction/sourcecode/exp4j/mutantInfo.json')
# m.copy_file("D:/mutationtestingReduction/expData/exp4j-exp4j-0.4.8/target/pit-reports/","D:/mutationtestingReduction/FeatureExtract/sourcecode/exp4j")