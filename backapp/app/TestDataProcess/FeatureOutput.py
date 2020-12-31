import csv
class FeatureOutput:
    def mutantToFile(self,outputpath,mutants):
        res=[]
        for mutant in mutants:
            # 过滤无用数据
            if getattr(mutant,mutant.CCAVCC)!=None:
                metrics=[]
                for feature in mutant.FEATURES:
                    metrics.append(getattr(mutant,feature))
                res.append(metrics)

        # 写文件
        with open(outputpath, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            header = ["numCovered","numTestsCover","mutantAssert","classAssert",
                      "mmCOMP", "mmNOCL", "mmNOS", "mmHLTH", "mmHVOC","mmHEFF", "mmHBUG", "mmCREF", "mmXMET",
                      "mmLMET", "mmNLOC", "mmNOC", "mmNOA", "mmMOD","mmHDIF", "mmVDEC", "mmEXCT", "mmEXCR",
                      "mmCAST", "mmTDN", "mmHVOL", "mmNAND", "mmVREF", "mmNOPR", "mmMDN", "mmNEXP", "mmLOOP",
                      "ccNoMethods", "ccLCOM", "ccAVCC", "ccNOS", "ccHBUG", "ccHEFF", "ccUWCS", "ccINST",
                      "ccPACK", "ccRFC", "ccCBO", "ccMI", "ccCCML", "ccNLOC", "ccRVF", "ccF-IN", "ccDIT",
                      "ccMINC", "ccS-R", "ccR-R", "ccCOH", "ccLMC", "ccLCOM2", "ccMAXCC", "ccHVOL", "ccHIER",
                      "ccNQU", "ccFOUT", "ccSuperclass", "ccSIX", "ccEXT", "ccNSUP", "ccTCC", "ccNSUB", "ccMPC",
                      "ccNCO", "ccINTR", "ccCCOM", "ccHLTH", "ccMOD",
                      "ppNoClasses", "ppNOS", "ppAVCC", "ppHBUG", "ppHEFF", "ppHLTH", "ppHVOL", "ppMI","ppCCML",
                      "ppNLOC", "ppRVF", "ppTCC", "ppCCOM", "ppINST", "ppDIST", "ppFIN","ppNoMethods", "ppMINC",
                      "ppABST", "ppMAXCC", "ppFOUT",
                      "operator", "methodReturn", "isKilled", "killTest", "rowNum", "fullclass", "fullmethod","key"]
            writer.writerow(header)
            # 写入多行用writerows
            writer.writerows(res)
            print("特征文件写入成功！")
