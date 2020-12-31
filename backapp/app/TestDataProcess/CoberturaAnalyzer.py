import os

class CoberturaAnalyzer:
    def parseHtml(self,dir):
        dirpath = os.path.join(dir,"cobertura")
        dir = os.listdir(dirpath)
        lineCovMap={}
        res={}
        for file in dir:
            if file.endswith(".html") and not file.startswith("frame") and file!="index.html" and file!="help.html":
                path = os.path.join(dirpath,file)
                fname=file[:-5].lower()
                f = open(path, "r")
                lines = f.readlines()
                for line in lines:
                    if line.find("numLineCover")>=0:
                        temp = line.split("numLineCover")[1].split("nbsp")[1]
                        lineNumber = int(temp[1:temp.index("<")])
                        if line.find("nbHitsCovered")>=0:
                            temp = line.split("nbHitsCovered")[1].split("nbsp")[1]
                            cover = int(temp[1:temp.index("<")])
                            lineCovMap[lineNumber]=cover
                        elif line.find("nbHitsUncovered")>=0:
                            temp = line.split("nbHitsUncovered")[1].split("nbsp")[1]
                            cover = int(temp[1:temp.index("<")])
                            lineCovMap[lineNumber] = cover
                        else:
                            print("[ERROR]"+line)
                res[fname]=lineCovMap
        return res

    def analyze(self,dir,mutants):
        coverageMap = self.parseHtml(dir)
        # print(coverageMap)
        total = 0
        for mutant in mutants:
            total+=1
            name = getattr(mutant,mutant.FULLCLASS).split("$")[0]
            try:
                if getattr(mutant,"status")=="NO_COVERAGE":
                    setattr(mutant,mutant.NUMCOVERED,"0")
                else:
                    setattr(mutant,mutant.NUMCOVERED,coverageMap[name].get(int(getattr(mutant,"lineNumber"))))
            except:
                print("[ERROR]"+mutant)

