import pandas as pd
import datetime
import csv
class FeatureConverse:
    def process_data(self,srcfile,optfile):
        # 读文件
        df = pd.read_csv(srcfile, delimiter=",", quoting=csv.QUOTE_NONE, encoding='utf-8')
        print(df.describe())
        all_len=df.shape[0]         #变异体总数
        # # 划分成90% 80% 70% 60% 50%各占20%
        # 划分成90% 80% 70% 60% 50% 40% 30% 20% 10%
        size=all_len//9
        opType=len(set(df['operator'].tolist()))
        mdType=len(set(df['methodReturn'].tolist()))
        mdNum=len(set(df['fullmethod'].tolist()))
        classNum=len(set(df['fullclass'].tolist()))
        allTest=df['killTest'].tolist()
        # ReductionRatio=[0.9,0.8,0.7,0.6,0.5]
        ReductionRatio = [0.9,0.8,0.7,0.6,0.5, 0.4, 0.3, 0.2, 0.1]
        features=list(df.columns)
        data = []
        for ratio in ReductionRatio:
            for i in range(size):
                trainEle= df.sample(frac=ratio)
                # print(trainEle.shape[0])
                row=[]
                ms=0
                for feature in features:
                    # numcovered特征出现了许多大数
                    if feature not in ['ccSuperclass', 'operator', 'methodReturn', 'isKilled', 'killTest', 'rowNum', 'fullclass','fullmethod', 'key']:
                        row.append(trainEle[feature].mean())
                    elif feature in ['operator', 'methodReturn','fullclass','fullmethod']:
                        subNum=len(set(trainEle[feature].tolist()))/len(set(df[feature].tolist()))
                        row.append(subNum)
                    elif feature=="killTest":
                        subset=set(trainEle[feature].tolist())
                        cnt=0
                        for t in allTest:
                            if t in subset:
                                cnt+=1
                        ms=cnt/len(allTest)
                row.append(ms)
                # print(row)
                data.append(row)
        # print(data)
        dataset = pd.DataFrame(data,columns=['numCovered', 'numTestsCover', 'mutantAssert', 'classAssert', 'mmCOMP', 'mmNOCL', 'mmNOS', 'mmHLTH', 'mmHVOC', 'mmHEFF', 'mmHBUG', 'mmCREF', 'mmXMET', 'mmLMET', 'mmNLOC', 'mmNOC', 'mmNOA', 'mmMOD', 'mmHDIF', 'mmVDEC', 'mmEXCT', 'mmEXCR', 'mmCAST', 'mmTDN', 'mmHVOL', 'mmNAND', 'mmVREF', 'mmNOPR', 'mmMDN', 'mmNEXP', 'mmLOOP', 'ccNoMethods', 'ccLCOM', 'ccAVCC', 'ccNOS', 'ccHBUG', 'ccHEFF', 'ccUWCS', 'ccINST', 'ccPACK', 'ccRFC', 'ccCBO', 'ccMI', 'ccCCML', 'ccNLOC', 'ccRVF', 'ccF-IN', 'ccDIT', 'ccMINC', 'ccS-R', 'ccR-R', 'ccCOH', 'ccLMC', 'ccLCOM2', 'ccMAXCC', 'ccHVOL', 'ccHIER', 'ccNQU', 'ccFOUT', 'ccSIX', 'ccEXT', 'ccNSUP', 'ccTCC', 'ccNSUB', 'ccMPC', 'ccNCO', 'ccINTR', 'ccCCOM', 'ccHLTH', 'ccMOD', 'ppNoClasses', 'ppNOS', 'ppAVCC', 'ppHBUG', 'ppHEFF', 'ppHLTH', 'ppHVOL', 'ppMI', 'ppCCML', 'ppNLOC', 'ppRVF', 'ppTCC', 'ppCCOM', 'ppINST', 'ppDIST', 'ppFIN', 'ppNoMethods', 'ppMINC', 'ppABST', 'ppMAXCC', 'ppFOUT', 'operator', 'methodReturn', 'fullclass', 'fullmethod', 'mscore'])  # 这时候是以行为标准写入的
        # print(dataset)
        dataset.to_csv(optfile)

