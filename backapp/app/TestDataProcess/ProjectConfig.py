import os
class ProjectConfig:
    # 项目配置
    def projectStart(self, path):
        # os.chdir(path)
        # print(os.popen('mvn clean').read())
        print('测试开始')
        # try:
        #     os.chdir(path)
        #     info = os.popen('mvn clean').read()
        #     # 触发异常
        #     if (info.find('BUILD FAILURE') >= 0):
        #         # 将错误信息传递给用户
        #         raise Exception(info)
        #     else:
        #         # 打印输出，方便开发者了解运行进度
        #         print(info)
        # except Exception as e:
        #     print('Error in project initialization')
        #     print(e)
        #     # 因为出现错误，所以非正常退出，后面语句不执行了
        #     exit(1)
        os.chdir(path)
        info = os.popen('mvn clean').read()
        # 触发异常
        if (info.find('BUILD FAILURE') >= 0):
            # 将错误信息传递给用户
            raise Exception(info)
        else:
            # 打印输出，方便开发者了解运行进度
            print(info)
        print('测试结束')