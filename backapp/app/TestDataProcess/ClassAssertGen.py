import os

class ClassAssertGen:
    def __init__(self,testpath=None,classpath=None,rootdir=None):
        self.targetfiles = dict()
        self.testfiles = dict()
        self.paths = []
        self.testpath = testpath
        self.classpath =classpath
        self.path = os.path.abspath(testpath)
        self.path2 = os.path.abspath(classpath)
        filepath=os.path.join(rootdir, "classResult.txt")
        self.output = open(filepath, "w+")
    def isclass(self,line):
        if "class" not in line.split(" "):
            return False
        return ("class" in line or 'interface' in line) and "{" in line and ".class" not in line and "*" not in line and "\"" not in line

    def ismethod(self,line):
        return "{" in line and "public" in line or "protected" in line or "private" in line

    def istargetfile(self,file):
        file = file.replace("Test", '')
        return file in self.targetfiles.keys()

    def linenum(self,file):
        file = file.replace("Test", '')
        return self.targetfiles[file]

    def analysis(self,file):
        input = open(file, 'r', encoding='UTF-8')
        count = 0
        for line in input:
            count += line.count("assert")
        return count

    def classline(self,file):
        # print(file)
        input = open(file, 'r', encoding='UTF-8')
        classcount = 0
        start = 0
        tmp = 0
        end = 0
        classname = ''
        index = 0
        for line in input:
            tmp += 1
            end += 1
            if self.isclass(line):
                line = line.split(" ")
                if "class" in line:
                    index = line.index("class")
                elif "index" in line:
                    index = line.index("interface")
                classname = line[index + 1]
                classcount += 1
                start = tmp
        self.output.write(classname + "," + str(start) + "--" + str(end) + '\n')
        self.output.write("total classes = " + str(classcount) + '\n')

    def classassertInfoGen(self):
        for root, dirs, files in os.walk(self.path2):
            for f in files:
                if ".java" not in f:
                    continue
                newpath = root + "/" + f
                self.paths.append(newpath)
                self.targetfiles[f] = 0

        for root, dirs, files in os.walk(self.path):
            for f in files:
                if ".java" not in f:
                    continue
                newpath = root + "/" + f
                print(newpath)
                self.testfiles[f] = newpath

        for file in self.targetfiles.keys():
            count = 0
            for path in self.paths:
                if file in path:
                    self.output.write(path + "\n")
                    self.classline(path)
                    break
            for testfile in self.testfiles.keys():
                if file.replace(".java", '') in testfile:
                    count += self.analysis(self.testfiles[testfile])
                    self.targetfiles[file] = 1
            self.output.write(file.replace(".java", '') + "," + str(count) + '\n')

        for (key, value) in self.targetfiles.items():
            if value == 0:
                for path in self.paths:
                    if key in path:
                        self.output.write(path + "\n")
                        break
        self.output.close()
