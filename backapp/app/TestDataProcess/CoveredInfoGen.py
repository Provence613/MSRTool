import os
import shutil

class CoveredInfo:
    def coveredInfoGen(self,path):
        # os.chdir(path)
        # print(os.popen('mvn test').read())
        print('测试开始')
        # try:
        #     os.chdir(path)
        #     info = os.popen('mvn test').read()
        #     # 触发异常
        #     if (info.find('BUILD FAILURE') >= 0):
        #         # 将错误信息传递给用户
        #         raise Exception(info)
        #     else:
        #         # 打印输出，方便开发者了解运行进度
        #         print(info)
        # except Exception as e:
        #     print('Error in coveredInfo generation')
        #     print(e)
        #     # 因为出现错误，所以非正常退出，后面语句不执行了
        #     exit(1)
        os.chdir(path)
        info = os.popen('mvn test').read()
        # 触发异常
        if (info.find('BUILD FAILURE') >= 0):
            # 将错误信息传递给用户
            raise Exception(info)
        else:
            # 打印输出，方便开发者了解运行进度
            print(info)

        print('测试结束')
    # 测试覆盖信息转储
    def copy_file(self,srcfilepath, desDir):
        shutil.copy(srcfilepath, desDir)
    # 解析stmt-cov.txt转换至coverage.txt
    def parse(self,dir):
        path = os.path.join(dir, "stmt-cov.txt")
        f = open(path, "r")
        lines = f.readlines()
        testset={}
        stmtset={}
        allmethods=set()
        testmethod=""
        for line in lines:
            if line.startswith("[TEST]"):
                testmethod=line[7:-1]
                methods=set()
                testset[testmethod]=methods
            else:
                testset.get(testmethod).add(line)
                allmethods.add(line)

        for md in allmethods:
            for testmd in testset:
                mdset=testset[testmd]
                if md in mdset:
                    if md not in stmtset:
                        testmethods = set()
                        stmtset[md]= testmethods
                    stmtset.get(md).add(testmd)

        outputpath= os.path.join(dir, "coverage.txt")
        f = open(outputpath, 'w')
        for key in stmtset:
            f.write(key.strip()+"=["+",".join(str(x) for x in list(stmtset.get(key)))+"]"+"\n")




