import os
import shutil

class ExecutedInfoGen:
    # 执行信息生成
    def executedInfoGen(self, path):
        # os.chdir(path)
        # print(os.popen('mvn cobertura:cobertura').read())
        print('测试开始')
        # try:
        #     os.chdir(path)
        #     info = os.popen('mvn cobertura:cobertura').read()
        #     # 触发异常
        #     if (info.find('BUILD FAILURE') >= 0):
        #         # 将错误信息传递给用户
        #         raise Exception(info)
        #     else:
        #         # 打印输出，方便开发者了解运行进度
        #         print(info)
        # except Exception as e:
        #     print('Error in executedinfo generation')
        #     print(e)
        #     # 因为出现错误，所以非正常退出，后面语句不执行了
        #     exit(1)
        os.chdir(path)
        info = os.popen('mvn cobertura:cobertura').read()
        # 触发异常
        if (info.find('BUILD FAILURE') >= 0):
            # 将错误信息传递给用户
            raise Exception(info)
        else:
            # 打印输出，方便开发者了解运行进度
            print(info)
        print('测试结束')

    # 执行信息转储
    def copy_file(self, srcDir, desDir):
        # path:"D:\mutationtestingReduction\expData\java-apns-0c13a8626967d4b4cfacab4afbcd840ee714ead8\target\site"
        # 创建文件夹
        # 判断路径是否存在
        if os.path.exists(srcDir):
            desdirpath = os.path.join(desDir, "cobertura")
            # 拷贝
            shutil.copytree(srcDir,desdirpath)
        else:
            print('[ERROR]')
