import pandas as pd
import csv
import os
import json

class ResultProcess:
    def conversefile(self,filepath,optpath):
        df = pd.read_csv(filepath, delimiter=",", quoting=csv.QUOTE_NONE, encoding='utf-8')
        newdf=df.reindex(columns=['rowNum','fullclass','fullmethod','operator'])
        res=[]
        for i, r in newdf.iterrows():
            mutantdic = {}
            mutantdic['id']=i+1
            mutantdic["RowNumber"]=r[0]
            mutantdic["ClassName"]=r[1]
            mutantdic['MethodName']=r[2].split('.')[-1]
            mutantdic['Operator']=r[3]
            res.append(mutantdic)
        # 写入json
        jsondic = {}
        jsondic['results'] = res
        file = open(optpath, 'w', encoding='utf-8')
        json.dump(jsondic, file, ensure_ascii=False)
        file.close()


