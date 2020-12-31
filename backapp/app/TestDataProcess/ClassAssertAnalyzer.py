import os
from TestDataProcess.Utils import Utils

class ClassAssertAnalyzer:
    def analyzer(self,dir,mutants):
        path = os.path.join(dir, "classResult.txt")
        f = open(path, "r")
        lines = f.readlines()
        classAssertDic={}
        for line in lines:
            if line.find(".java")>0:
                utils=Utils()
                fullClassName=utils.getClassNameFromDir(line) + ".java"
                continue
            if line.find("--")>=0 or line.find("total classes")>=0:
                continue
            try:
                classAssertDic[fullClassName] = line.split(",")[1]
            except:
                print("[ERROR]"+line)

        for mutant in mutants:
            val = classAssertDic.get(getattr(mutant,"javaFileName"));
            if val == None:
                # print(getattr(mutant,"javaFileName"))
                val = 0
            setattr(mutant,mutant.CLASS_ASSERT,int(val))

