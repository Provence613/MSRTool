import numpy as np
import random
import pandas as pd
import timeit
from math import log10
import pickle
import csv
import os

class MSReduceForGA:
    def process_data(self,df,indexList,getTest=False):
        allTest=df['killTest'].tolist()
        features=list(df.columns)
        data = []
        testSize=0
        for idx in indexList:
            trainEle=df.loc[idx]
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
                    if getTest:
                        testSize=len(subset)
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
        # 处理特征
        featuresTwo = ['numCovered', 'numTestsCover', 'mutantAssert', 'classAssert']
        for feature in list(dataset.columns):
            arr = dataset[feature].values.tolist()
            for i in range(len(arr)):
                if feature != "isKilled":
                    if feature in featuresTwo and float(arr[i]) > 1.0:
                        arr[i] = log10(float(arr[i])) / log10(1.2)
                    else:
                        arr[i] = float(arr[i])
            dataset[feature] = pd.DataFrame(arr)
        x, y = dataset.iloc[:, :-1].values, dataset.iloc[:, -1].values
        return x.tolist(),y.tolist(),testSize

    # 种群初始化
    def getInitialPopulation(self,chromosomeSize,populationSize,boundarylist):
        population=np.zeros((populationSize,chromosomeSize),dtype=np.uint8)
        indexList=[]
        initialList=range(chromosomeSize)
        low,high=boundarylist
        for i in range(populationSize):
            shuffle=random.sample(initialList,int(chromosomeSize*0.1*random.randint(low,high)))
            indexList.append(shuffle)
            for j in shuffle:
                population[i,j]=1
            # print(population[i,:])
        return population,indexList

    # 染色体解码得到表现型的解
    def decodedChromosome(self,population):
        indexList=[]
        for pop in population:
            indexList.append([index for (index, value) in enumerate(list(pop)) if value == 1])
        return indexList

    # 求解种群的适应度值
    def getFittnessValue(self,model,indexList,df):
        x,y,temp=self.process_data(df,indexList)
        # print(len(x[0]))
        # print(mean_squared_error(y, model.MutantSetReduce(x)))
        fitnessvalues=model.predict(x)
        fitnessvalues=np.array([fitnessvalues])
        fitnessvalues=fitnessvalues.reshape(-1,1)
        # 计算每个染色体被选择的概率
        probability = fitnessvalues / np.sum(fitnessvalues)
        # 得到每个染色体被选中的累积概率
        cum_probability = np.cumsum(probability)
        # print("fitnessvalues", fitnessvalues)
        # print("cum_probability", cum_probability)
        return fitnessvalues, cum_probability

    # 新种群选择
    def selectNewPopulation(self,chromosomes, cum_probability):
        m, n = chromosomes.shape
        newpopulation = np.zeros((m, n), dtype=np.uint8)
        # print("new",newpopulation)
        # 随机产生M个概率值
        randoms = np.random.rand(m)
        for i, randoma in enumerate(randoms):
            logical = cum_probability >= randoma
            index = np.where(logical == 1)
            # index是tuple,tuple中元素是ndarray
            newpopulation[i, :] = chromosomes[index[0][0], :]
        return newpopulation
        pass

    # 新种群交叉
    def crossover(self,population, Pc=0.8):
        """
        :param population: 新种群
        :param Pc: 交叉概率默认是0.8
        :return: 交叉后得到的新种群
        """
        # 根据交叉概率计算需要进行交叉的个体个数
        m, n = population.shape
        numbers = np.uint8(m * Pc)
        # 确保进行交叉的染色体个数是偶数个
        if numbers % 2 != 0:
            numbers += 1
        # 交叉后得到的新种群
        updatepopulation = np.zeros((m, n), dtype=np.uint8)
        # 产生随机索引
        index = random.sample(range(m), numbers)
        # 不进行交叉的染色体进行复制
        for i in range(m):
            if not index.__contains__(i):
                updatepopulation[i, :] = population[i, :]
        # crossover
        while len(index) > 0:
            a = index.pop()
            b = index.pop()
            # 随机产生一个交叉点
            crossoverPoint = random.sample(range(1, n), 1)
            crossoverPoint = crossoverPoint[0]
            # one-single-point crossover
            updatepopulation[a, 0:crossoverPoint] = population[a, 0:crossoverPoint]
            updatepopulation[a, crossoverPoint:] = population[b, crossoverPoint:]
            updatepopulation[b, 0:crossoverPoint] = population[b, 0:crossoverPoint]
            updatepopulation[b, crossoverPoint:] = population[a, crossoverPoint:]
        return updatepopulation
        pass

    # 染色体变异
    def mutation(self,population, Pm=0.01):
        """
        :param population: 经交叉后得到的种群
        :param Pm: 变异概率默认是0.01
        :return: 经变异操作后的新种群
        """
        updatepopulation = np.copy(population)
        m, n = population.shape
        # 计算需要变异的基因个数
        gene_num = np.uint8(m * n * Pm)
        # 将所有的基因按照序号进行10进制编码，则共有m*n个基因
        # 随机抽取gene_num个基因进行基本位变异
        mutationGeneIndex = random.sample(range(0, m * n), gene_num)
        # 确定每个将要变异的基因在整个染色体中的基因座(即基因的具体位置)
        for gene in mutationGeneIndex:
            # 确定变异基因位于第几个染色体
            chromosomeIndex = gene // n
            # 确定变异基因位于当前染色体的第几个基因位
            geneIndex = gene % n
            # mutation
            if updatepopulation[chromosomeIndex, geneIndex] == 0:
                updatepopulation[chromosomeIndex, geneIndex] = 1
            else:
                updatepopulation[chromosomeIndex, geneIndex] = 0
        # print("update:",updatepopulation)
        return updatepopulation
        pass

    def run(self,filepath,modelpath,boundarylist,max_iter=10,populationSize=50):
        # 每次迭代得到的最优解
        optimalSolutions = []
        optimalValues = []
        # 约简比例的取值范围（通过训练集得知）
        # boundarylist=[4,6]
        # 得到染色体编码长度
        df = pd.read_csv(filepath, delimiter=",", quoting=csv.QUOTE_NONE, encoding='utf-8')
        mutationSize = df.shape[0] - 1  # 变异体总数
        # 获取预测变异体集合质量的预测模型
        with open(modelpath, "rb") as f:
            model = pickle.load(f)
        # 得到初始种群编码
        population, indexList = self.getInitialPopulation(mutationSize, populationSize, boundarylist)
        # 生成初始种群时已获得indexList,故不需要种群解码
        for iteration in range(max_iter):
            # 得到个体适应度值和个体的累积概率
            evalvalues, cum_proba = self.getFittnessValue(model,indexList,df)
            # 选择新的种群
            newpopulations = self.selectNewPopulation(population, cum_proba)
            # 进行交叉操作
            crossoverpopulation = self.crossover(newpopulations)
            # mutation
            mutationpopulation = self.mutation(crossoverpopulation)
            totalpopulation=np.vstack((population,mutationpopulation))
            nextpopulation=self.getNextpopulation(totalpopulation,model,populationSize,df)
            # 将变异后的种群解码，得到每轮迭代最终的种群的indexList
            finalIndexList = self.decodedChromosome(nextpopulation)
            # 适应度评价
            fitnessvalues, cum_individual_proba = self.getFittnessValue(model,finalIndexList,df)
            # 搜索每次迭代的最优解，以及最优解对应的目标函数的取值
            optimalValues.append(np.max(list(fitnessvalues)))
            index = np.where(fitnessvalues == max(list(fitnessvalues)))
            optimalSolutions.append(nextpopulation[index[0][0], :])
            population=nextpopulation
        # 搜索最优解
        optimalValue = np.max(optimalValues)
        optimalIndex = np.where(optimalValues == optimalValue)
        optimalSolution = optimalSolutions[optimalIndex[0][0]]
        return optimalSolution, optimalValue,mutationSize,df
    
    def getNextpopulation(self,totalpopulation,model,populationSize,df):
        nextpopulation=[]
        newIndexList=self.decodedChromosome(totalpopulation)
        fitnessvalues, cum_individual_proba = self.getFittnessValue(model, newIndexList, df)
        fitvlist = list(fitnessvalues)
        fitvlist.sort(reverse=True)
        for i in range(populationSize):
            index = np.where(fitnessvalues == fitvlist[i][0])
            nextpopulation.append(totalpopulation[index[0][0], :])
        nextpopulation=np.array(nextpopulation)
        # print(type(nextpopulation))
        return nextpopulation

    def outputRes(self,solution,value,size,df,reduceRespath):
        print('最优解:')
        # print(solution)
        solutionlist = solution.tolist()
        solutionidx = [i for i, x in enumerate(solutionlist) if x == 1]
        solutiondf = df.loc[solutionidx]
        print(solutiondf)
        solutiondf.to_csv(reduceRespath, index=False, header=True)
        newSize = list(solution).count(1)
        print('约简后的变异体:', newSize)
        print('约简比例:', 1 - float(newSize / size))
        print('最优目标函数值:', value)
        # 计算测试充分度
        resIndexList = self.decodedChromosome(np.array([solution]))
        x, y, testSize = self.process_data(df, resIndexList, True)
        print('测试充分度:', y[0])
        print('测试用例数', testSize)
        return newSize,y[0],testSize




