import os
import csv

class Utils:
    def getClassNameFromDir(self,line):
        # 特殊字符处理
        line = line.replace('\\', '/')
        line = line.replace('\n', '/n')
        line = line.replace('\r', '/r')
        line = line.replace('\t', '/t')
        dir = line.split('/')
        fullClassName = ""
        for i in range(len(dir)-1,-1,-1):
            string = dir[i]
            if string!="src" and string!="java" and string!="main" and string!="test":
                fullClassName = string + "." + fullClassName
            else:
                break
        fullClassName = fullClassName[0:-8].lower()
        return fullClassName