import bs4
import os
import csv

class StaticMetricGen:
    # 静态特征生成
    def staticmetricGen(self, toolpath,projectdir,rootdir):
        # os.chdir(toolpath)
        # cmd = "java -jar JHawkCommandLine.jar -f .*\\.java -r -l pcm -s " + projectdir + "\\src\\main -hp  " + rootdir + "\\StaticMetricHtml -h index"
        # print(os.popen(cmd).read())
        print('测试开始')
        # try:
        #     os.chdir(toolpath)
        #     cmd = "java -jar JHawkCommandLine.jar -f .*\\.java -r -l pcm -s " + projectdir + "\\src\\main -hp  " + rootdir + "\\StaticMetricHtml -h index"
        #     info = os.popen(cmd).read()
        #     # 触发异常
        #     if (info.find('Exception') >= 0):
        #         # 将错误信息传递给用户
        #         raise Exception(info)
        #     else:
        #         # 打印输出，方便开发者了解运行进度
        #         print(info)
        # except Exception as e:
        #     print('Error in static metric generation')
        #     print(e)
        #     # 因为出现错误，所以非正常退出，后面语句不执行了
        #     exit(1)
        os.chdir(toolpath)
        cmd = "java -jar JHawkCommandLine.jar -f .*\\.java -r -l pcm -s " + projectdir + "\\src\\main -hp  " + rootdir + "\\StaticMetricHtml -h index"
        info = os.popen(cmd).read()
        # 触发异常
        if (info.find('Exception') >= 0):
            # 将错误信息传递给用户
            raise Exception(info)
        else:
            # 打印输出，方便开发者了解运行进度
            print(info)
        print('测试结束')
    def parseHtml(self,rootdir):
        res=[]
        dirpath = os.path.join(rootdir,"StaticMetricHtml")
        dir = os.listdir(dirpath)
        for file in dir:
            if file.endswith(".html"):
                path = os.path.join(dirpath, file)
                name = file[0:file.rindex(".")]
                f = open(path)
                html=bs4.BeautifulSoup(f.read(), 'html5lib')
                table= html.select('table')[3]
                trs=table.select("tr")
                header=trs[0].select("th")[0].get_text()
                # print(header)
                flag=""
                if header.find("Packages in System")>=0:
                    flag="pkg"
                elif header.find("Classes in Package")>=0:
                    flag="class"
                else:
                    flag="method"
                # 遍历该表格内的所有的tr
                for i in range(1,len(trs)):
                    info=[]
                    tr=trs[i]
                    ths=tr.select("th")
                    for j in range(1,len(ths)):
                        th=ths[j]
                        text=th.get_text()
                        info.append(text)
                    tds=tr.select("td")
                    if len(tds)>0:
                        if flag=="method":
                            info.append(name[0:name.rindex(".")])
                            info.append(name[name.rindex(".")+1:])
                        elif flag=="class":
                            info.append(name)
                        for j in range(1,len(tds)):
                            td = tds[j]
                            # 获取文本信息
                            text = td.get_text()
                            info.append(text)
                        res.append(info)

        self.writeCSV(rootdir,res)

    def writeCSV(self,dir,res):
        pkgres=[]
        classres=[]
        methodres=[]
        # 提取数据
        for list in res:
            length=len(list)
            if length == 22:
                pkgres.append(list)
            elif length == 42:
                classres.append(list)
            elif length == 30:
                methodres.append(list)
        # 合并
        res=[]
        for md in methodres:
            pkgname=md[0]
            classname=md[1]
            for cls in classres:
                if cls[0]==pkgname and cls[1]==classname:
                    md.extend(cls[2:])
            for pkg in  pkgres:
                if pkg[0]==pkgname:
                    md.extend(pkg[1:])
            res.append(md)
        # 写文件
        outputpath= os.path.join(dir,"staticMetrics.csv")
        with open(outputpath, "w",newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            header=["pkgName","className","mdName", "mmCOMP", "mmNOCL", "mmNOS", "mmHLTH", "mmHVOC", "mmHEFF", "mmHBUG", "mmCREF", "mmXMET", "mmLMET", "mmNLOC", "mmNOC", "mmNOA", "mmMOD", "mmHDIF", "mmVDEC", "mmEXCT", "mmEXCR", "mmCAST", "mmTDN", "mmHVOL", "mmNAND", "mmVREF", "mmNOPR", "mmMDN", "mmNEXP", "mmLOOP",
                    "ccNoMethods", "ccLCOM", "ccAVCC", "ccNOS", "ccHBUG", "ccHEFF", "ccUWCS", "ccINST", "ccPACK", "ccRFC", "ccCBO", "ccMI", "ccCCML", "ccNLOC", "ccRVF", "ccF-IN", "ccDIT", "ccMINC", "ccS-R", "ccR-R", "ccCOH", "ccLMC", "ccLCOM2", "ccMAXCC", "ccHVOL", "ccHIER", "ccNQU", "ccFOUT", "ccSuperclass", "ccSIX", "ccEXT", "ccNSUP", "ccTCC", "ccNSUB", "ccMPC", "ccNCO", "ccINTR", "ccCCOM", "ccHLTH", "ccMOD",
                    "ppNoClasses", "ppNOS", "ppAVCC", "ppHBUG", "ppHEFF", "ppHLTH", "ppHVOL", "ppMI", "ppCCML", "ppNLOC", "ppRVF", "ppTCC", "ppCCOM", "ppINST", "ppDIST", "ppFIN", "ppNoMethods", "ppMINC", "ppABST", "ppMAXCC", "ppFOUT"]
            writer.writerow(header)
            # 写入多行用writerows
            writer.writerows(res)

