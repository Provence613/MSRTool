import os

class MethodAssertGen:
    def __init__(self,testpath=None,rootdir=None):
        # testpath="D:\mutationtestingReduction\expData\msgpack-java-9f48d2f80a29a63cd7b7142ee61e64f167f7d402/src/test"
        self.testpath=testpath
        self.path = os.path.abspath(testpath)
        filepath = os.path.join(rootdir, "testMethodResult.txt")
        self.output = open(filepath, "w+")


    def isclass(self,line):
        return "class" in line and "{" in line and ".class" not in line


    def ismethod(self,line):
        return line.find("test")!=-1 and ("{" in line and "public" in line or "protected" in line or "private" in line)


    def analysis(self,file):
        input = open(file,'r', encoding='UTF-8')
        currentclass = ''
        currentmethod = ''
        count = 0
        self.output.write(file + "\n")
        for line in input:
            # print(line)
            if (self.isclass(line)):
                line = line.split(" ")
                try:
                    index = line.index("class")
                except Exception:
                    continue

                if currentclass != '' and currentmethod != '':
                    self.output.write(currentclass + "," + currentmethod + "," + str(count) + '\n')
                currentclass = line[index + 1]
                currentmethod = ''
                count = 0
                continue
            elif (self.ismethod(line)):
                end = line.rfind(")") + 1
                middle = line.find("(")
                start = line.rfind(" ", 0, middle) + 1
                if currentclass != '' and currentmethod != '':
                    self.output.write(currentclass + "," + currentmethod + "," + str(count) + '\n')
                currentmethod = line[start:end]
                count = 0
                continue
            count += line.count("assert")
        if currentclass != '' and currentmethod != '':
            self.output.write(currentclass + "," + currentmethod + "," + str(count) + '\n')

    def methodassertGen(self):
        for root, dirs, files in os.walk(self.path):
            for f in files:
                if ".java" not in f:
                    continue
                newpath = root + "/" + f
                print(newpath)
                self.analysis(newpath)
                self.output.write("\n")
        self.output.close()
